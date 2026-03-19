#include "xr/xr_runtime.h"

#include "common/log.h"
#include "renderer/vk_context.h"

#include <android/native_window.h>
#include <android/native_window_jni.h>
#include <cstring>
#include <sstream>
#include <string>
#include <vector>

namespace {

constexpr const char* kLogTag = "TeleopXrSession";

std::string FormatXrResult(XrInstance instance, XrResult result) {
    if (instance == XR_NULL_HANDLE) {
        return std::to_string(result);
    }

    char buffer[XR_MAX_RESULT_STRING_SIZE];
    buffer[0] = '\0';
    xrResultToString(instance, result, buffer);
    return buffer;
}

bool CheckXr(XrInstance instance, XrResult result, const char* step, std::string* error) {
    if (XR_SUCCEEDED(result)) {
        return true;
    }

    if (error != nullptr) {
        *error = std::string(step) + " failed with " + FormatXrResult(instance, result);
    }
    return false;
}

const char* SessionStateToString(XrSessionState state) {
    switch (state) {
        case XR_SESSION_STATE_UNKNOWN:
            return "unknown";
        case XR_SESSION_STATE_IDLE:
            return "idle";
        case XR_SESSION_STATE_READY:
            return "ready";
        case XR_SESSION_STATE_SYNCHRONIZED:
            return "synchronized";
        case XR_SESSION_STATE_VISIBLE:
            return "visible";
        case XR_SESSION_STATE_FOCUSED:
            return "focused";
        case XR_SESSION_STATE_STOPPING:
            return "stopping";
        case XR_SESSION_STATE_LOSS_PENDING:
            return "loss-pending";
        case XR_SESSION_STATE_EXITING:
            return "exiting";
        default:
            return "other";
    }
}

bool LoadPassthroughFunctions(teleop::xr::Runtime* runtime, std::string* error) {
    return CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrCreatePassthroughFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_create_passthrough_fb)),
               "xrGetInstanceProcAddr(xrCreatePassthroughFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrDestroyPassthroughFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_destroy_passthrough_fb)),
               "xrGetInstanceProcAddr(xrDestroyPassthroughFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrPassthroughStartFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_passthrough_start_fb)),
               "xrGetInstanceProcAddr(xrPassthroughStartFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrPassthroughPauseFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_passthrough_pause_fb)),
               "xrGetInstanceProcAddr(xrPassthroughPauseFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrCreatePassthroughLayerFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_create_passthrough_layer_fb)),
               "xrGetInstanceProcAddr(xrCreatePassthroughLayerFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrDestroyPassthroughLayerFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(
                       &runtime->xr_destroy_passthrough_layer_fb)),
               "xrGetInstanceProcAddr(xrDestroyPassthroughLayerFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrPassthroughLayerResumeFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(
                       &runtime->xr_passthrough_layer_resume_fb)),
               "xrGetInstanceProcAddr(xrPassthroughLayerResumeFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrPassthroughLayerPauseFB",
                   reinterpret_cast<PFN_xrVoidFunction*>(&runtime->xr_passthrough_layer_pause_fb)),
               "xrGetInstanceProcAddr(xrPassthroughLayerPauseFB)",
               error) &&
           CheckXr(
               runtime->instance,
               xrGetInstanceProcAddr(
                   runtime->instance,
                   "xrCreateSwapchainAndroidSurfaceKHR",
                   reinterpret_cast<PFN_xrVoidFunction*>(
                       &runtime->xr_create_swapchain_android_surface_khr)),
               "xrGetInstanceProcAddr(xrCreateSwapchainAndroidSurfaceKHR)",
               error);
}

bool StartPassthrough(teleop::xr::Runtime* runtime, std::string* error) {
    if (runtime->passthrough_running || runtime->passthrough == XR_NULL_HANDLE ||
        runtime->passthrough_layer == XR_NULL_HANDLE) {
        return true;
    }

    // Passthrough and layer were created with XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB,
    // so they are already running — just mark the state and resume the layer.
    XrResult layer_result = runtime->xr_passthrough_layer_resume_fb(runtime->passthrough_layer);
    if (!XR_SUCCEEDED(layer_result)) {
        teleop::common::LogError(
            kLogTag,
            ("xrPassthroughLayerResumeFB failed with " +
             FormatXrResult(runtime->instance, layer_result))
                .c_str());
        // Non-fatal: continue without passthrough
        return true;
    }

    runtime->passthrough_running = true;
    teleop::common::LogInfo(kLogTag, "Passthrough layer resumed successfully");
    return true;
}

void PausePassthrough(teleop::xr::Runtime* runtime) {
    if (!runtime->passthrough_running) {
        return;
    }

    runtime->xr_passthrough_layer_pause_fb(runtime->passthrough_layer);
    runtime->xr_passthrough_pause_fb(runtime->passthrough);
    runtime->passthrough_running = false;
}

void DrawQuadTestPattern(ANativeWindow* window, int32_t width, int32_t height) {
    if (window == nullptr) {
        return;
    }

    ANativeWindow_setBuffersGeometry(window, width, height, WINDOW_FORMAT_RGBA_8888);

    ANativeWindow_Buffer buffer{};
    if (ANativeWindow_lock(window, &buffer, nullptr) != 0) {
        return;
    }

    auto* pixels = static_cast<uint32_t*>(buffer.bits);
    if (pixels == nullptr) {
        ANativeWindow_unlockAndPost(window);
        return;
    }

    const int32_t border = 24;
    for (int32_t y = 0; y < buffer.height; ++y) {
        for (int32_t x = 0; x < buffer.width; ++x) {
            const bool in_border =
                x < border || y < border || x >= buffer.width - border ||
                y >= buffer.height - border;
            const uint8_t blue = static_cast<uint8_t>(120 + (100 * x) / buffer.width);
            const uint8_t green = static_cast<uint8_t>(70 + (90 * y) / buffer.height);
            const uint8_t red = in_border ? 20 : 8;
            const uint32_t color =
                0xFF000000u | (static_cast<uint32_t>(red) << 16) |
                (static_cast<uint32_t>(green) << 8) | static_cast<uint32_t>(blue);
            pixels[y * buffer.stride + x] = color;
        }
    }

    // Paint a bright center strip so the test panel is obvious in-headset.
    const int32_t strip_top = buffer.height / 2 - 18;
    const int32_t strip_bottom = buffer.height / 2 + 18;
    const int32_t strip_left = buffer.width / 4;
    const int32_t strip_right = buffer.width * 3 / 4;
    for (int32_t y = strip_top; y < strip_bottom; ++y) {
        for (int32_t x = strip_left; x < strip_right; ++x) {
            pixels[y * buffer.stride + x] = 0xFFF0F0F0u;
        }
    }

    ANativeWindow_unlockAndPost(window);
}

bool CreateQuadPanelSurface(teleop::xr::Runtime* runtime, std::string* error) {
    if (runtime->xr_create_swapchain_android_surface_khr == nullptr) {
        if (error != nullptr) {
            *error = "xrCreateSwapchainAndroidSurfaceKHR was unavailable";
        }
        return false;
    }

    XrSwapchainCreateInfo create_info{XR_TYPE_SWAPCHAIN_CREATE_INFO};
    create_info.usageFlags = XR_SWAPCHAIN_USAGE_SAMPLED_BIT | XR_SWAPCHAIN_USAGE_COLOR_ATTACHMENT_BIT;
    create_info.format = 0;
    create_info.sampleCount = 0;
    create_info.width = static_cast<uint32_t>(runtime->quad_width);
    create_info.height = static_cast<uint32_t>(runtime->quad_height);
    create_info.faceCount = 0;
    create_info.arraySize = 0;
    create_info.mipCount = 0;

    JNIEnv* env = nullptr;
    bool should_detach = false;
    if (runtime->vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK) {
        if (runtime->vm->AttachCurrentThread(&env, nullptr) != JNI_OK || env == nullptr) {
            if (error != nullptr) {
                *error = "AttachCurrentThread failed for quad swapchain surface";
            }
            return false;
        }
        should_detach = true;
    }

    jobject surface = nullptr;
    if (!CheckXr(
            runtime->instance,
            runtime->xr_create_swapchain_android_surface_khr(
                runtime->session,
                &create_info,
                &runtime->quad_swapchain,
                &surface),
            "xrCreateSwapchainAndroidSurfaceKHR",
            error)) {
        if (should_detach) {
            runtime->vm->DetachCurrentThread();
        }
        return false;
    }

    runtime->quad_window = ANativeWindow_fromSurface(env, surface);
    env->DeleteGlobalRef(surface);
    if (should_detach) {
        runtime->vm->DetachCurrentThread();
    }

    if (runtime->quad_window == nullptr) {
        if (error != nullptr) {
            *error = "ANativeWindow_fromSurface returned null";
        }
        return false;
    }

    DrawQuadTestPattern(runtime->quad_window, runtime->quad_width, runtime->quad_height);
    runtime->quad_layer_ready = true;
    return true;
}

}  // namespace

namespace teleop::xr {

bool CreateSession(
    Runtime* runtime,
    const teleop::renderer::VulkanContext& vk_context,
    std::string* error) {
    if (runtime == nullptr || runtime->instance == XR_NULL_HANDLE || !vk_context.ready) {
        if (error != nullptr) {
            *error = "CreateSession called before OpenXR/Vulkan initialization finished";
        }
        return false;
    }

    XrGraphicsBindingVulkanKHR graphics_binding{XR_TYPE_GRAPHICS_BINDING_VULKAN_KHR};
    graphics_binding.instance = vk_context.instance;
    graphics_binding.physicalDevice = vk_context.physical_device;
    graphics_binding.device = vk_context.device;
    graphics_binding.queueFamilyIndex = vk_context.graphics_queue_family_index;
    graphics_binding.queueIndex = vk_context.graphics_queue_index;

    XrSessionCreateInfo session_create_info{XR_TYPE_SESSION_CREATE_INFO};
    session_create_info.next = &graphics_binding;
    session_create_info.systemId = runtime->system_id;

    if (!CheckXr(
            runtime->instance,
            xrCreateSession(runtime->instance, &session_create_info, &runtime->session),
            "xrCreateSession",
            error)) {
        return false;
    }

    XrReferenceSpaceCreateInfo space_create_info{XR_TYPE_REFERENCE_SPACE_CREATE_INFO};
    space_create_info.referenceSpaceType = XR_REFERENCE_SPACE_TYPE_LOCAL;
    space_create_info.poseInReferenceSpace.orientation.w = 1.0f;
    if (!CheckXr(
            runtime->instance,
            xrCreateReferenceSpace(runtime->session, &space_create_info, &runtime->app_space),
            "xrCreateReferenceSpace",
            error)) {
        DestroySession(runtime);
        return false;
    }

    if (runtime->passthrough_supported) {
        if (!LoadPassthroughFunctions(runtime, error)) {
            DestroySession(runtime);
            return false;
        }

        XrPassthroughCreateInfoFB passthrough_create_info{XR_TYPE_PASSTHROUGH_CREATE_INFO_FB};
        passthrough_create_info.flags = XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB;
        if (!CheckXr(
                runtime->instance,
                runtime->xr_create_passthrough_fb(
                    runtime->session,
                    &passthrough_create_info,
                    &runtime->passthrough),
                "xrCreatePassthroughFB",
                error)) {
            DestroySession(runtime);
            return false;
        }

        XrPassthroughLayerCreateInfoFB layer_create_info{
            XR_TYPE_PASSTHROUGH_LAYER_CREATE_INFO_FB};
        layer_create_info.passthrough = runtime->passthrough;
        layer_create_info.flags = XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB;
        layer_create_info.purpose = XR_PASSTHROUGH_LAYER_PURPOSE_RECONSTRUCTION_FB;
        if (!CheckXr(
                runtime->instance,
                runtime->xr_create_passthrough_layer_fb(
                    runtime->session,
                    &layer_create_info,
                    &runtime->passthrough_layer),
                "xrCreatePassthroughLayerFB",
                error)) {
            DestroySession(runtime);
            return false;
        }
    }

    if (!CreateQuadPanelSurface(runtime, error)) {
        DestroySession(runtime);
        return false;
    }

    runtime->session_ready = true;
    runtime->session_state = XR_SESSION_STATE_IDLE;
    runtime->exit_render_loop = false;
    runtime->frame_count = 0;
    common::LogInfo(kLogTag, "OpenXR session created.");
    return true;
}

void DestroySession(Runtime* runtime) {
    if (runtime == nullptr) {
        return;
    }

    // First, ensure passthrough is cleaned up safely
    if (runtime->passthrough_running) {
        PausePassthrough(runtime);
    }

    if (runtime->passthrough_layer != XR_NULL_HANDLE &&
        runtime->xr_destroy_passthrough_layer_fb != nullptr) {
        // Safe cleanup of passthrough layer
        std::string error;
        if (XR_SUCCEEDED(runtime->xr_destroy_passthrough_layer_fb(runtime->passthrough_layer))) {
            teleop::common::LogInfo(kLogTag, "Passthrough layer destroyed successfully");
        } else {
            teleop::common::LogError(kLogTag, "Failed to destroy passthrough layer gracefully");
        }
        runtime->passthrough_layer = XR_NULL_HANDLE;
    }

    if (runtime->passthrough != XR_NULL_HANDLE && runtime->xr_destroy_passthrough_fb != nullptr) {
        // Safe cleanup of passthrough
        if (XR_SUCCEEDED(runtime->xr_destroy_passthrough_fb(runtime->passthrough))) {
            teleop::common::LogInfo(kLogTag, "Passthrough destroyed successfully");
        } else {
            teleop::common::LogError(kLogTag, "Failed to destroy passthrough gracefully");
        }
        runtime->passthrough = XR_NULL_HANDLE;
    }

    // End session if running
    if (runtime->session != XR_NULL_HANDLE) {
        if (runtime->session_running) {
            XrResult end_result = xrEndSession(runtime->session);
            if (XR_SUCCEEDED(end_result)) {
                teleop::common::LogInfo(kLogTag, "Session ended successfully");
            } else {
                teleop::common::LogError(kLogTag, "Failed to end session gracefully");
            }
            runtime->session_running = false;
        }

        // Destroy reference space first
        if (runtime->app_space != XR_NULL_HANDLE) {
            XrResult space_result = xrDestroySpace(runtime->app_space);
            if (XR_SUCCEEDED(space_result)) {
                teleop::common::LogInfo(kLogTag, "App space destroyed successfully");
            } else {
                teleop::common::LogError(kLogTag, "Failed to destroy app space");
            }
            runtime->app_space = XR_NULL_HANDLE;
        }

        // Destroy swapchain
        if (runtime->quad_swapchain != XR_NULL_HANDLE) {
            XrResult swapchain_result = xrDestroySwapchain(runtime->quad_swapchain);
            if (XR_SUCCEEDED(swapchain_result)) {
                teleop::common::LogInfo(kLogTag, "Swapchain destroyed successfully");
            } else {
                teleop::common::LogError(kLogTag, "Failed to destroy swapchain");
            }
            runtime->quad_swapchain = XR_NULL_HANDLE;
        }

        // Finally, destroy the session
        XrResult session_result = xrDestroySession(runtime->session);
        if (XR_SUCCEEDED(session_result)) {
            teleop::common::LogInfo(kLogTag, "Session destroyed successfully");
        } else {
            teleop::common::LogError(kLogTag, "Failed to destroy session");
        }
        runtime->session = XR_NULL_HANDLE;
    }

    // Clean up native window
    if (runtime->quad_window != nullptr) {
        ANativeWindow_release(runtime->quad_window);
        runtime->quad_window = nullptr;
    }

    // Reset all state
    runtime->session_state = XR_SESSION_STATE_UNKNOWN;
    runtime->session_running = false;
    runtime->session_ready = false;
    runtime->passthrough_running = false;
    runtime->quad_layer_ready = false;
    runtime->exit_render_loop = false;
    runtime->frame_count = 0;
}

bool PumpEvents(Runtime* runtime, std::string* error) {
    if (runtime == nullptr || runtime->instance == XR_NULL_HANDLE) {
        if (error != nullptr) {
            *error = "PumpEvents called before xrCreateInstance";
        }
        return false;
    }

    XrEventDataBuffer event_buffer{XR_TYPE_EVENT_DATA_BUFFER};
    while (true) {
        const XrResult result = xrPollEvent(runtime->instance, &event_buffer);
        if (result == XR_EVENT_UNAVAILABLE) {
            return true;
        }

        if (!CheckXr(runtime->instance, result, "xrPollEvent", error)) {
            return false;
        }

        switch (event_buffer.type) {
            case XR_TYPE_EVENT_DATA_INSTANCE_LOSS_PENDING:
                runtime->exit_render_loop = true;
                break;
            case XR_TYPE_EVENT_DATA_SESSION_STATE_CHANGED: {
                const auto* changed =
                    reinterpret_cast<const XrEventDataSessionStateChanged*>(&event_buffer);
                runtime->session_state = changed->state;

                if (changed->state == XR_SESSION_STATE_READY && !runtime->session_running) {
                    XrSessionBeginInfo begin_info{XR_TYPE_SESSION_BEGIN_INFO};
                    begin_info.primaryViewConfigurationType =
                        XR_VIEW_CONFIGURATION_TYPE_PRIMARY_STEREO;
                    if (!CheckXr(
                            runtime->instance,
                            xrBeginSession(runtime->session, &begin_info),
                            "xrBeginSession",
                            error)) {
                        return false;
                    }
                    // Try to start passthrough, but don't fail if it doesn't work
                    std::string passthrough_error;
                    if (!StartPassthrough(runtime, &passthrough_error)) {
                        teleop::common::LogError(
                            kLogTag, 
                            ("Passthrough failed: " + passthrough_error).c_str());
                        // Continue anyway - app can work without passthrough
                    }
                    runtime->session_running = true;
                } else if (
                    changed->state == XR_SESSION_STATE_STOPPING && runtime->session_running) {
                    PausePassthrough(runtime);
                    if (!CheckXr(
                            runtime->instance,
                            xrEndSession(runtime->session),
                            "xrEndSession",
                            error)) {
                        return false;
                    }
                    runtime->session_running = false;
                } else if (
                    changed->state == XR_SESSION_STATE_EXITING ||
                    changed->state == XR_SESSION_STATE_LOSS_PENDING) {
                    runtime->exit_render_loop = true;
                }
                break;
            }
            default:
                break;
        }

        event_buffer = {XR_TYPE_EVENT_DATA_BUFFER};
    }
}

std::string DescribeSession(const Runtime* runtime) {
    if (runtime == nullptr) {
        return "xr.session=runtime-null";
    }

    std::ostringstream stream;
    stream << "xr.session=" << (runtime->session_ready ? "created" : "not-created")
           << " running=" << (runtime->session_running ? "true" : "false")
           << " state=" << SessionStateToString(runtime->session_state)
           << " passthrough=" << (runtime->passthrough_running ? "on" : "off")
           << " quad=" << (runtime->quad_layer_ready ? "ready" : "off");
    return stream.str();
}

}  // namespace teleop::xr
