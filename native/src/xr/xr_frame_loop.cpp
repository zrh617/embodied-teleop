#include "xr/xr_runtime.h"

#include "video/video_texture_bridge.h"

#include <sstream>
#include <string>

namespace {

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

bool RenderFrame(Runtime* runtime, std::string* error) {
    if (runtime == nullptr || !runtime->session_running) {
        return true;
    }

    XrFrameWaitInfo frame_wait_info{XR_TYPE_FRAME_WAIT_INFO};
    XrFrameState frame_state{XR_TYPE_FRAME_STATE};
    if (!CheckXr(
            runtime->instance,
            xrWaitFrame(runtime->session, &frame_wait_info, &frame_state),
            "xrWaitFrame",
            error)) {
        return false;
    }

    XrFrameBeginInfo frame_begin_info{XR_TYPE_FRAME_BEGIN_INFO};
    if (!CheckXr(
            runtime->instance,
            xrBeginFrame(runtime->session, &frame_begin_info),
            "xrBeginFrame",
            error)) {
        return false;
    }

    XrFrameEndInfo frame_end_info{XR_TYPE_FRAME_END_INFO};
    frame_end_info.displayTime = frame_state.predictedDisplayTime;
    frame_end_info.environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_OPAQUE;
    XrCompositionLayerPassthroughFB passthrough_layer{
        XR_TYPE_COMPOSITION_LAYER_PASSTHROUGH_FB};
    passthrough_layer.flags = XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT;
    passthrough_layer.space = XR_NULL_HANDLE;
    passthrough_layer.layerHandle = runtime->passthrough_layer;

    XrCompositionLayerQuad quad_layer{XR_TYPE_COMPOSITION_LAYER_QUAD};
    quad_layer.layerFlags = XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT;
    quad_layer.space = runtime->app_space;
    quad_layer.eyeVisibility = XR_EYE_VISIBILITY_BOTH;
    quad_layer.subImage.swapchain = runtime->quad_swapchain;
    quad_layer.subImage.imageRect.offset = {0, 0};
    quad_layer.subImage.imageRect.extent = {runtime->quad_width, runtime->quad_height};
    quad_layer.subImage.imageArrayIndex = 0;
    quad_layer.pose.orientation.w = 1.0f;
    quad_layer.pose.position.x = 0.0f;
    quad_layer.pose.position.y = 0.05f;
    quad_layer.pose.position.z = -1.2f;
    quad_layer.size.width = 1.6f;
    quad_layer.size.height = 0.9f;

    const XrCompositionLayerBaseHeader* layers[2];
    uint32_t layer_count = 0;
    if (runtime->passthrough_running && runtime->passthrough_layer != XR_NULL_HANDLE) {
        layers[layer_count++] =
            reinterpret_cast<const XrCompositionLayerBaseHeader*>(&passthrough_layer);
    }
    if (runtime->quad_layer_ready && runtime->quad_swapchain != XR_NULL_HANDLE &&
        runtime->app_space != XR_NULL_HANDLE) {
        // Draw the latest video frame into the quad surface every frame.
        // Falls back to keeping whatever was last drawn if no new frame arrived.
        teleop::video::DrawVideoFrameToWindow(runtime->quad_window);
        layers[layer_count++] =
            reinterpret_cast<const XrCompositionLayerBaseHeader*>(&quad_layer);
    }

    frame_end_info.layerCount = layer_count;
    frame_end_info.layers = layer_count > 0 ? layers : nullptr;

    if (!CheckXr(
            runtime->instance,
            xrEndFrame(runtime->session, &frame_end_info),
            "xrEndFrame",
            error)) {
        return false;
    }

    ++runtime->frame_count;
    return true;
}

std::string DescribeFrameLoop(const Runtime* runtime) {
    if (runtime == nullptr) {
        return "xr.frame_loop=runtime-null";
    }

    std::ostringstream stream;
    stream << "xr.frame_loop=session_running=" << (runtime->session_running ? "true" : "false")
           << " frame_count=" << runtime->frame_count;
    return stream.str();
}

}  // namespace teleop::xr
