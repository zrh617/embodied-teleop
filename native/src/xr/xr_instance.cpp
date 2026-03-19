#include "xr/xr_runtime.h"

#include "common/log.h"

#include <array>
#include <cstdio>
#include <sstream>
#include <string>

namespace {

constexpr const char* kLogTag = "TeleopXrInstance";

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

}  // namespace

namespace teleop::xr {

bool CreateInstance(JavaVM* vm, jobject activity, Runtime* runtime, std::string* error) {
    if (runtime == nullptr || vm == nullptr || activity == nullptr) {
        if (error != nullptr) {
            *error = "CreateInstance received a null runtime/vm/activity";
        }
        common::LogError(kLogTag, "CreateInstance: null parameters detected");
        return false;
    }

    *runtime = {};
    runtime->vm = vm;
    common::LogInfo(kLogTag, "CreateInstance: starting OpenXR initialization");

    PFN_xrInitializeLoaderKHR initialize_loader = nullptr;
    XrResult result = xrGetInstanceProcAddr(
        XR_NULL_HANDLE,
        "xrInitializeLoaderKHR",
        reinterpret_cast<PFN_xrVoidFunction*>(&initialize_loader));
    if (XR_FAILED(result) || initialize_loader == nullptr) {
        if (error != nullptr) {
            *error = "xrInitializeLoaderKHR was unavailable";
        }
        common::LogError(kLogTag, "Failed to get xrInitializeLoaderKHR");
        return false;
    }
    common::LogInfo(kLogTag, "xrInitializeLoaderKHR obtained successfully");

    XrLoaderInitInfoAndroidKHR loader_init_info{XR_TYPE_LOADER_INIT_INFO_ANDROID_KHR};
    loader_init_info.applicationVM = vm;
    loader_init_info.applicationContext = activity;
    result = initialize_loader(
        reinterpret_cast<const XrLoaderInitInfoBaseHeaderKHR*>(&loader_init_info));
    if (!CheckXr(XR_NULL_HANDLE, result, "xrInitializeLoaderKHR", error)) {
        common::LogError(kLogTag, "xrInitializeLoaderKHR initialization failed");
        return false;
    }
    runtime->loader_initialized = true;
    common::LogInfo(kLogTag, "OpenXR loader initialized");

    const std::array<const char*, 4> required_extensions = {
        XR_KHR_ANDROID_CREATE_INSTANCE_EXTENSION_NAME,
        XR_KHR_ANDROID_SURFACE_SWAPCHAIN_EXTENSION_NAME,
        XR_KHR_VULKAN_ENABLE2_EXTENSION_NAME,
        XR_FB_PASSTHROUGH_EXTENSION_NAME,
    };

    XrInstanceCreateInfo create_info{XR_TYPE_INSTANCE_CREATE_INFO};
    XrInstanceCreateInfoAndroidKHR android_create_info{
        XR_TYPE_INSTANCE_CREATE_INFO_ANDROID_KHR};
    android_create_info.applicationVM = vm;
    android_create_info.applicationActivity = activity;
    create_info.next = &android_create_info;
    create_info.applicationInfo.applicationVersion = 1;
    create_info.applicationInfo.engineVersion = 1;
    create_info.applicationInfo.apiVersion = XR_CURRENT_API_VERSION;
    std::snprintf(
        create_info.applicationInfo.applicationName,
        XR_MAX_APPLICATION_NAME_SIZE,
        "%s",
        "QuestTeleop");
    std::snprintf(
        create_info.applicationInfo.engineName,
        XR_MAX_ENGINE_NAME_SIZE,
        "%s",
        "teleop");
    create_info.enabledExtensionCount = static_cast<uint32_t>(required_extensions.size());
    create_info.enabledExtensionNames = required_extensions.data();

    if (!CheckXr(
            XR_NULL_HANDLE,
            xrCreateInstance(&create_info, &runtime->instance),
            "xrCreateInstance",
            error)) {
        common::LogError(kLogTag, "Failed to create XR instance");
        return false;
    }
    common::LogInfo(kLogTag, "XR instance created successfully");

    XrSystemGetInfo system_info{XR_TYPE_SYSTEM_GET_INFO};
    system_info.formFactor = XR_FORM_FACTOR_HEAD_MOUNTED_DISPLAY;
    if (!CheckXr(
            runtime->instance,
            xrGetSystem(runtime->instance, &system_info, &runtime->system_id),
            "xrGetSystem",
            error)) {
        common::LogError(kLogTag, "Failed to get XR system");
        DestroyInstance(runtime);
        return false;
    }
    common::LogInfo(kLogTag, "XR system obtained successfully");

    runtime->instance_ready = true;
    runtime->passthrough_supported = true;
    common::LogInfo(kLogTag, "OpenXR instance created successfully.");
    return true;
}

void DestroyInstance(Runtime* runtime) {
    if (runtime == nullptr) {
        return;
    }

    if (runtime->instance != XR_NULL_HANDLE) {
        xrDestroyInstance(runtime->instance);
    }

    *runtime = {};
}

std::string DescribeInstance(const Runtime* runtime) {
    if (runtime == nullptr) {
        return "xr.instance=runtime-null";
    }

    std::ostringstream stream;
    stream << "xr.instance="
           << (runtime->instance_ready ? "ready" : (runtime->loader_initialized ? "loader-ready"
                                                                                 : "cold"))
           << " system_id=" << runtime->system_id;
    return stream.str();
}

}  // namespace teleop::xr
