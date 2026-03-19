#pragma once

#include <string>

#include <jni.h>
#include <vulkan/vulkan.h>
#include <openxr/openxr_platform.h>

namespace teleop::renderer {

struct VulkanContext {
    VkInstance instance = VK_NULL_HANDLE;
    VkPhysicalDevice physical_device = VK_NULL_HANDLE;
    VkDevice device = VK_NULL_HANDLE;
    VkQueue graphics_queue = VK_NULL_HANDLE;
    uint32_t graphics_queue_family_index = 0;
    uint32_t graphics_queue_index = 0;
    bool ready = false;
};

bool CreateVulkanContext(
    XrInstance xr_instance,
    XrSystemId system_id,
    VulkanContext* context,
    std::string* error);

void DestroyVulkanContext(VulkanContext* context);

std::string DescribeVulkanContext(const VulkanContext* context);
std::string DescribeCurvedScreen();
std::string DescribeVideoPipeline();
std::string DescribeHudRenderer();

}  // namespace teleop::renderer
