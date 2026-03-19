#include "renderer/vk_context.h"

#include "common/log.h"

#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

namespace {

constexpr const char* kLogTag = "TeleopVulkan";

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

uint32_t FindGraphicsQueueFamily(VkPhysicalDevice physical_device) {
    uint32_t queue_family_count = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(physical_device, &queue_family_count, nullptr);
    if (queue_family_count == 0) {
        return UINT32_MAX;
    }

    std::vector<VkQueueFamilyProperties> queue_families(queue_family_count);
    vkGetPhysicalDeviceQueueFamilyProperties(
        physical_device,
        &queue_family_count,
        queue_families.data());

    for (uint32_t i = 0; i < queue_family_count; ++i) {
        if ((queue_families[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) != 0) {
            return i;
        }
    }

    return UINT32_MAX;
}

}  // namespace

namespace teleop::renderer {

bool CreateVulkanContext(
    XrInstance xr_instance,
    XrSystemId system_id,
    VulkanContext* context,
    std::string* error) {
    if (context == nullptr) {
        if (error != nullptr) {
            *error = "VulkanContext was null";
        }
        return false;
    }

    *context = {};

    PFN_xrGetVulkanGraphicsRequirements2KHR get_graphics_requirements = nullptr;
    PFN_xrCreateVulkanInstanceKHR create_vulkan_instance = nullptr;
    PFN_xrGetVulkanGraphicsDevice2KHR get_vulkan_graphics_device = nullptr;
    PFN_xrCreateVulkanDeviceKHR create_vulkan_device = nullptr;

    if (!CheckXr(
            xr_instance,
            xrGetInstanceProcAddr(
                xr_instance,
                "xrGetVulkanGraphicsRequirements2KHR",
                reinterpret_cast<PFN_xrVoidFunction*>(&get_graphics_requirements)),
            "xrGetInstanceProcAddr(xrGetVulkanGraphicsRequirements2KHR)",
            error) ||
        !CheckXr(
            xr_instance,
            xrGetInstanceProcAddr(
                xr_instance,
                "xrCreateVulkanInstanceKHR",
                reinterpret_cast<PFN_xrVoidFunction*>(&create_vulkan_instance)),
            "xrGetInstanceProcAddr(xrCreateVulkanInstanceKHR)",
            error) ||
        !CheckXr(
            xr_instance,
            xrGetInstanceProcAddr(
                xr_instance,
                "xrGetVulkanGraphicsDevice2KHR",
                reinterpret_cast<PFN_xrVoidFunction*>(&get_vulkan_graphics_device)),
            "xrGetInstanceProcAddr(xrGetVulkanGraphicsDevice2KHR)",
            error) ||
        !CheckXr(
            xr_instance,
            xrGetInstanceProcAddr(
                xr_instance,
                "xrCreateVulkanDeviceKHR",
                reinterpret_cast<PFN_xrVoidFunction*>(&create_vulkan_device)),
            "xrGetInstanceProcAddr(xrCreateVulkanDeviceKHR)",
            error)) {
        return false;
    }

    XrGraphicsRequirementsVulkan2KHR graphics_requirements{
        XR_TYPE_GRAPHICS_REQUIREMENTS_VULKAN2_KHR};
    if (!CheckXr(
            xr_instance,
            get_graphics_requirements(xr_instance, system_id, &graphics_requirements),
            "xrGetVulkanGraphicsRequirements2KHR",
            error)) {
        return false;
    }

    uint32_t selected_api_version =
        static_cast<uint32_t>(graphics_requirements.maxApiVersionSupported);
    if (selected_api_version == 0) {
        selected_api_version = VK_API_VERSION_1_1;
    }

    VkApplicationInfo app_info{VK_STRUCTURE_TYPE_APPLICATION_INFO};
    app_info.pApplicationName = "QuestTeleop";
    app_info.applicationVersion = VK_MAKE_VERSION(0, 1, 0);
    app_info.pEngineName = "teleop";
    app_info.engineVersion = VK_MAKE_VERSION(0, 1, 0);
    app_info.apiVersion = selected_api_version;

    VkInstanceCreateInfo instance_create_info{VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO};
    instance_create_info.pApplicationInfo = &app_info;

    XrVulkanInstanceCreateInfoKHR xr_instance_create_info{
        XR_TYPE_VULKAN_INSTANCE_CREATE_INFO_KHR};
    xr_instance_create_info.systemId = system_id;
    xr_instance_create_info.pfnGetInstanceProcAddr = &vkGetInstanceProcAddr;
    xr_instance_create_info.vulkanCreateInfo = &instance_create_info;
    xr_instance_create_info.vulkanAllocator = nullptr;

    VkResult vk_result = VK_SUCCESS;
    if (!CheckXr(
            xr_instance,
            create_vulkan_instance(
                xr_instance,
                &xr_instance_create_info,
                &context->instance,
                &vk_result),
            "xrCreateVulkanInstanceKHR",
            error)) {
        return false;
    }

    if (vk_result != VK_SUCCESS) {
        if (error != nullptr) {
            *error = "xrCreateVulkanInstanceKHR returned VkResult " + std::to_string(vk_result);
        }
        return false;
    }

    XrVulkanGraphicsDeviceGetInfoKHR graphics_device_info{
        XR_TYPE_VULKAN_GRAPHICS_DEVICE_GET_INFO_KHR};
    graphics_device_info.systemId = system_id;
    graphics_device_info.vulkanInstance = context->instance;

    if (!CheckXr(
            xr_instance,
            get_vulkan_graphics_device(
                xr_instance,
                &graphics_device_info,
                &context->physical_device),
            "xrGetVulkanGraphicsDevice2KHR",
            error)) {
        DestroyVulkanContext(context);
        return false;
    }

    context->graphics_queue_family_index = FindGraphicsQueueFamily(context->physical_device);
    if (context->graphics_queue_family_index == UINT32_MAX) {
        if (error != nullptr) {
            *error = "No Vulkan graphics queue family was available";
        }
        DestroyVulkanContext(context);
        return false;
    }

    const float queue_priority = 1.0f;
    VkDeviceQueueCreateInfo queue_create_info{VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO};
    queue_create_info.queueFamilyIndex = context->graphics_queue_family_index;
    queue_create_info.queueCount = 1;
    queue_create_info.pQueuePriorities = &queue_priority;

    VkPhysicalDeviceFeatures enabled_features{};

    VkDeviceCreateInfo device_create_info{VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO};
    device_create_info.queueCreateInfoCount = 1;
    device_create_info.pQueueCreateInfos = &queue_create_info;
    device_create_info.pEnabledFeatures = &enabled_features;

    XrVulkanDeviceCreateInfoKHR xr_device_create_info{XR_TYPE_VULKAN_DEVICE_CREATE_INFO_KHR};
    xr_device_create_info.systemId = system_id;
    xr_device_create_info.pfnGetInstanceProcAddr = &vkGetInstanceProcAddr;
    xr_device_create_info.vulkanPhysicalDevice = context->physical_device;
    xr_device_create_info.vulkanCreateInfo = &device_create_info;
    xr_device_create_info.vulkanAllocator = nullptr;

    if (!CheckXr(
            xr_instance,
            create_vulkan_device(
                xr_instance,
                &xr_device_create_info,
                &context->device,
                &vk_result),
            "xrCreateVulkanDeviceKHR",
            error)) {
        DestroyVulkanContext(context);
        return false;
    }

    if (vk_result != VK_SUCCESS) {
        if (error != nullptr) {
            *error = "xrCreateVulkanDeviceKHR returned VkResult " + std::to_string(vk_result);
        }
        DestroyVulkanContext(context);
        return false;
    }

    vkGetDeviceQueue(
        context->device,
        context->graphics_queue_family_index,
        context->graphics_queue_index,
        &context->graphics_queue);

    context->ready = context->graphics_queue != VK_NULL_HANDLE;
    if (!context->ready) {
        if (error != nullptr) {
            *error = "vkGetDeviceQueue returned a null graphics queue";
        }
        DestroyVulkanContext(context);
        return false;
    }

    teleop::common::LogInfo(kLogTag, "Vulkan context created for OpenXR session.");
    return true;
}

void DestroyVulkanContext(VulkanContext* context) {
    if (context == nullptr) {
        return;
    }

    if (context->device != VK_NULL_HANDLE) {
        vkDeviceWaitIdle(context->device);
        vkDestroyDevice(context->device, nullptr);
    }

    if (context->instance != VK_NULL_HANDLE) {
        vkDestroyInstance(context->instance, nullptr);
    }

    *context = {};
}

std::string DescribeVulkanContext(const VulkanContext* context) {
    if (context == nullptr || !context->ready) {
        return "renderer.vk=not-ready";
    }

    std::ostringstream stream;
    stream << "renderer.vk=ready queue_family=" << context->graphics_queue_family_index;
    return stream.str();
}

}  // namespace teleop::renderer
