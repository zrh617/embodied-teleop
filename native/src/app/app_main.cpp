#include "app/app_runtime.h"

#include "common/log.h"
#include "common/time.h"
#include "renderer/vk_context.h"
#include "xr/xr_runtime.h"

#include <chrono>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>

namespace teleop::video {
std::string DescribeTextureBridge();
std::string DescribeTiming();
}  // namespace teleop::video

namespace teleop::input {
std::string DescribePoseProvider();
std::string DescribeControllerInput();
}  // namespace teleop::input

namespace {

constexpr const char* kLogTag = "TeleopNative";

struct AppRuntimeState {
    std::mutex mutex;
    JavaVM* vm = nullptr;
    jobject activity = nullptr;
    bool initialized = false;
    bool resumed = false;
    bool stop_requested = false;
    bool exit_requested = false;
    bool thread_running = false;
    std::thread render_thread;
    std::string status = "runtime=cold";
    teleop::xr::Runtime xr_runtime;
    teleop::renderer::VulkanContext vk_context;
};

AppRuntimeState g_app;

void SetStatus(const std::string& status) {
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.status = status;
    }
    teleop::common::LogInfo(kLogTag, status.c_str());
}

bool ShouldStopRuntimeThread() {
    std::lock_guard<std::mutex> lock(g_app.mutex);
    return g_app.stop_requested || g_app.exit_requested;
}

void DestroyRuntimeObjects() {
    teleop::xr::DestroySession(&g_app.xr_runtime);
    teleop::renderer::DestroyVulkanContext(&g_app.vk_context);
    teleop::xr::DestroyInstance(&g_app.xr_runtime);
}

void RuntimeThreadMain() {
    SetStatus("runtime=bootstrapping-openxr");

    JavaVM* vm = nullptr;
    jobject activity = nullptr;
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        vm = g_app.vm;
        activity = g_app.activity;
    }

    std::string error;
    if (!teleop::xr::CreateInstance(vm, activity, &g_app.xr_runtime, &error)) {
        SetStatus("runtime=instance-error " + error);
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.thread_running = false;
        g_app.stop_requested = false;
        return;
    }

    if (!teleop::renderer::CreateVulkanContext(
            g_app.xr_runtime.instance,
            g_app.xr_runtime.system_id,
            &g_app.vk_context,
            &error)) {
        SetStatus("runtime=vulkan-error " + error);
        DestroyRuntimeObjects();
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.thread_running = false;
        g_app.stop_requested = false;
        return;
    }

    if (!teleop::xr::CreateSession(&g_app.xr_runtime, g_app.vk_context, &error)) {
        SetStatus("runtime=session-error " + error);
        DestroyRuntimeObjects();
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.thread_running = false;
        g_app.stop_requested = false;
        return;
    }

    SetStatus("runtime=session-created");

    while (!ShouldStopRuntimeThread() && !g_app.xr_runtime.exit_render_loop) {
        if (!teleop::xr::PumpEvents(&g_app.xr_runtime, &error)) {
            SetStatus("runtime=event-error " + error);
            break;
        }

        if (g_app.xr_runtime.exit_render_loop) {
            SetStatus("runtime=session-exit-requested");
            break;
        }

        if (g_app.xr_runtime.session_running) {
            if (!teleop::xr::RenderFrame(&g_app.xr_runtime, &error)) {
                SetStatus("runtime=frame-error " + error);
                break;
            }
        } else {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }

    DestroyRuntimeObjects();
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.thread_running = false;
        g_app.stop_requested = false;
        if (!g_app.exit_requested) {
            g_app.status = "runtime=stopped";
        }
    }
    teleop::common::LogInfo(kLogTag, "Runtime thread stopped.");
}

void StartRuntimeThreadIfNeeded() {
    std::lock_guard<std::mutex> lock(g_app.mutex);
    if (!g_app.initialized || !g_app.resumed || g_app.exit_requested || g_app.thread_running ||
        g_app.activity == nullptr) {
        return;
    }

    g_app.stop_requested = false;
    g_app.thread_running = true;
    g_app.render_thread = std::thread(RuntimeThreadMain);
}

void StopRuntimeThread() {
    std::thread render_thread;
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        if (!g_app.thread_running) {
            DestroyRuntimeObjects();
            return;
        }

        g_app.stop_requested = true;
        render_thread = std::move(g_app.render_thread);
    }

    if (render_thread.joinable()) {
        render_thread.join();
    }

    // Give a small delay to ensure XR thread has finished cleanup
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
}

std::string BuildStatus() {
    std::lock_guard<std::mutex> lock(g_app.mutex);

    std::ostringstream stream;
    stream << "native=" << (g_app.initialized ? "ready" : "cold")
           << " lifecycle=" << (g_app.resumed ? "resumed" : "paused")
           << " thread=" << (g_app.thread_running ? "running" : "stopped")
           << "\nstatus=" << g_app.status
           << "\nclock.ns=" << teleop::common::NowMonotonicNanos()
           << "\n" << teleop::xr::DescribeInstance(&g_app.xr_runtime)
           << "\n" << teleop::xr::DescribeSession(&g_app.xr_runtime)
           << "\n" << teleop::xr::DescribeFrameLoop(&g_app.xr_runtime)
           << "\n" << teleop::xr::DescribeActions(&g_app.xr_runtime)
           << "\n" << teleop::renderer::DescribeVulkanContext(&g_app.vk_context)
           << "\n" << teleop::renderer::DescribeCurvedScreen()
           << "\n" << teleop::renderer::DescribeVideoPipeline()
           << "\n" << teleop::renderer::DescribeHudRenderer()
           << "\n" << teleop::video::DescribeTextureBridge()
           << "\n" << teleop::video::DescribeTiming()
           << "\n" << teleop::input::DescribePoseProvider()
           << "\n" << teleop::input::DescribeControllerInput();
    return stream.str();
}

}  // namespace

namespace teleop::app {

bool Init(JavaVM* vm, jobject activity) {
    if (vm == nullptr || activity == nullptr) {
        teleop::common::LogError(kLogTag, "Init failed because vm or activity was null.");
        return false;
    }

    JNIEnv* env = nullptr;
    if (vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK || env == nullptr) {
        teleop::common::LogError(kLogTag, "Init failed because JNIEnv was unavailable.");
        return false;
    }

    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        if (g_app.activity != nullptr) {
            env->DeleteGlobalRef(g_app.activity);
        }
        g_app.vm = vm;
        g_app.activity = env->NewGlobalRef(activity);
        g_app.initialized = g_app.activity != nullptr;
        g_app.exit_requested = false;
        g_app.status = g_app.initialized ? "runtime=initialized" : "runtime=activity-ref-error";
        
        if (!g_app.initialized) {
            teleop::common::LogError(kLogTag, "Failed to create global reference to activity");
        }
    }

    if (g_app.initialized) {
        teleop::common::LogInfo(kLogTag, "Native app initialized from Kotlin successfully.");
    } else {
        teleop::common::LogError(kLogTag, "Native app initialization failed.");
    }
    
    return g_app.initialized;
}

void OnResume() {
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.resumed = true;
        g_app.stop_requested = false;
        g_app.status = "runtime=resuming";
    }
    teleop::common::LogInfo(kLogTag, "Lifecycle moved to resume.");
    StartRuntimeThreadIfNeeded();
}

void OnPause() {
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.resumed = false;
        g_app.status = "runtime=android-paused-keeping-xr-alive";
    }
    teleop::common::LogInfo(
        kLogTag,
        "Lifecycle moved to pause, but XR runtime stays alive for immersive handoff.");
}

void RequestExit() {
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        g_app.exit_requested = true;
        g_app.resumed = false;
        g_app.status = "runtime=exit-requested";
    }
    teleop::common::LogInfo(kLogTag, "Exit requested from Kotlin.");
    StopRuntimeThread();

    // Clean up JNI global references after XR thread is stopped
    {
        std::lock_guard<std::mutex> lock(g_app.mutex);
        if (g_app.activity != nullptr && g_app.vm != nullptr) {
            JNIEnv* env = nullptr;
            if (g_app.vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) == JNI_OK) {
                env->DeleteGlobalRef(g_app.activity);
                teleop::common::LogInfo(kLogTag, "Activity global reference released.");
            }
            g_app.activity = nullptr;
        }
        g_app.initialized = false;
    }
}

std::string GetStatus() {
    return BuildStatus();
}

std::string GetControllerStateJson() {
    bool left_active = g_app.xr_runtime.left_hand_active;
    bool right_active = g_app.xr_runtime.right_hand_active;
    XrPosef left_pose = g_app.xr_runtime.left_hand_pose;
    XrPosef right_pose = g_app.xr_runtime.right_hand_pose;

    const uint64_t ts_ms = teleop::common::NowMonotonicNanos() / 1000000ULL;

    std::ostringstream stream;
    stream << "{";
    stream << "\"type\":\"xr_controller_state\",";
    stream << "\"ts_ms\":" << ts_ms << ",";
    stream << "\"seq\":" << ts_ms << ",";
    stream << "\"head\":{";
    stream << "\"pos\":{\"x\":0.0,\"y\":0.0,\"z\":0.0},";
    stream << "\"rot\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":1.0}";
    stream << "},";

    stream << "\"left\":{";
    stream << "\"connected\":" << (left_active ? "true" : "false") << ",";
    stream << "\"pos\":{";
    stream << "\"x\":" << left_pose.position.x << ",";
    stream << "\"y\":" << left_pose.position.y << ",";
    stream << "\"z\":" << left_pose.position.z;
    stream << "},";
    stream << "\"rot\":{";
    stream << "\"x\":" << left_pose.orientation.x << ",";
    stream << "\"y\":" << left_pose.orientation.y << ",";
    stream << "\"z\":" << left_pose.orientation.z << ",";
    stream << "\"w\":" << left_pose.orientation.w;
    stream << "}";
    stream << "},";

    stream << "\"right\":{";
    stream << "\"connected\":" << (right_active ? "true" : "false") << ",";
    stream << "\"pos\":{";
    stream << "\"x\":" << right_pose.position.x << ",";
    stream << "\"y\":" << right_pose.position.y << ",";
    stream << "\"z\":" << right_pose.position.z;
    stream << "},";
    stream << "\"rot\":{";
    stream << "\"x\":" << right_pose.orientation.x << ",";
    stream << "\"y\":" << right_pose.orientation.y << ",";
    stream << "\"z\":" << right_pose.orientation.z << ",";
    stream << "\"w\":" << right_pose.orientation.w;
    stream << "}";
    stream << "}";
    stream << "}";

    return stream.str();
}

}  // namespace teleop::app
