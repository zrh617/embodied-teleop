#pragma once

#include <cstdint>
#include <string>

#include <android/native_window.h>
#include <jni.h>
#include <vulkan/vulkan.h>
#include <openxr/openxr_platform.h>

namespace teleop::renderer {
struct VulkanContext;
}

namespace teleop::xr {

struct Runtime {
    JavaVM* vm = nullptr;
    XrInstance instance = XR_NULL_HANDLE;
    XrSystemId system_id = XR_NULL_SYSTEM_ID;
    XrSession session = XR_NULL_HANDLE;
    XrSpace app_space = XR_NULL_HANDLE;
    XrPassthroughFB passthrough = XR_NULL_HANDLE;
    XrPassthroughLayerFB passthrough_layer = XR_NULL_HANDLE;
    XrSwapchain quad_swapchain = XR_NULL_HANDLE;
    ANativeWindow* quad_window = nullptr;
    XrSessionState session_state = XR_SESSION_STATE_UNKNOWN;
    bool loader_initialized = false;
    bool session_running = false;
    bool instance_ready = false;
    bool session_ready = false;
    bool passthrough_supported = false;
    bool passthrough_running = false;
    bool quad_layer_ready = false;
    bool exit_render_loop = false;
    uint64_t frame_count = 0;
    int32_t quad_width = 1024;
    int32_t quad_height = 1024;

    XrActionSet action_set = XR_NULL_HANDLE;
    XrAction hand_pose_action = XR_NULL_HANDLE;
    XrAction trigger_action = XR_NULL_HANDLE;
    XrAction squeeze_action = XR_NULL_HANDLE;
    XrAction thumbstick_action = XR_NULL_HANDLE;
    XrAction thumbstick_click_action = XR_NULL_HANDLE;
    XrAction button_a_action = XR_NULL_HANDLE;  // right A
    XrAction button_b_action = XR_NULL_HANDLE;  // right B
    XrAction button_x_action = XR_NULL_HANDLE;  // left X
    XrAction button_y_action = XR_NULL_HANDLE;  // left Y
    XrAction menu_action = XR_NULL_HANDLE;       // left menu
    XrPath left_hand_path = XR_NULL_PATH;
    XrPath right_hand_path = XR_NULL_PATH;
    XrSpace left_hand_space = XR_NULL_HANDLE;
    XrSpace right_hand_space = XR_NULL_HANDLE;
    bool actions_ready = false;

    bool left_hand_active = false;
    bool right_hand_active = false;
    XrPosef left_hand_pose{};
    XrPosef right_hand_pose{};

    // Per-hand analog/button state (updated every frame)
    float left_trigger = 0.f;
    float right_trigger = 0.f;
    float left_squeeze = 0.f;
    float right_squeeze = 0.f;
    float left_thumbstick_x = 0.f;
    float left_thumbstick_y = 0.f;
    float right_thumbstick_x = 0.f;
    float right_thumbstick_y = 0.f;
    bool left_thumbstick_click = false;
    bool right_thumbstick_click = false;
    bool button_a = false;   // right controller A
    bool button_b = false;   // right controller B
    bool button_x = false;   // left controller X
    bool button_y = false;   // left controller Y
    bool button_menu = false; // left controller menu

    PFN_xrCreatePassthroughFB xr_create_passthrough_fb = nullptr;
    PFN_xrDestroyPassthroughFB xr_destroy_passthrough_fb = nullptr;
    PFN_xrPassthroughStartFB xr_passthrough_start_fb = nullptr;
    PFN_xrPassthroughPauseFB xr_passthrough_pause_fb = nullptr;
    PFN_xrCreatePassthroughLayerFB xr_create_passthrough_layer_fb = nullptr;
    PFN_xrDestroyPassthroughLayerFB xr_destroy_passthrough_layer_fb = nullptr;
    PFN_xrPassthroughLayerResumeFB xr_passthrough_layer_resume_fb = nullptr;
    PFN_xrPassthroughLayerPauseFB xr_passthrough_layer_pause_fb = nullptr;
    PFN_xrCreateSwapchainAndroidSurfaceKHR xr_create_swapchain_android_surface_khr = nullptr;
};

bool CreateInstance(
    JavaVM* vm,
    jobject activity,
    Runtime* runtime,
    std::string* error);

void DestroyInstance(Runtime* runtime);

bool CreateSession(
    Runtime* runtime,
    const teleop::renderer::VulkanContext& vk_context,
    std::string* error);

void DestroySession(Runtime* runtime);

bool PumpEvents(Runtime* runtime, std::string* error);
bool RenderFrame(Runtime* runtime, std::string* error);

bool CreateActions(Runtime* runtime, std::string* error);
void DestroyActions(Runtime* runtime);
bool UpdateHandPoses(Runtime* runtime, XrTime display_time, std::string* error);

std::string DescribeInstance(const Runtime* runtime);
std::string DescribeSession(const Runtime* runtime);
std::string DescribeFrameLoop(const Runtime* runtime);
std::string DescribeActions(const Runtime* runtime);

}  // namespace teleop::xr
