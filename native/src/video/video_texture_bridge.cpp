#include "video/video_texture_bridge.h"

#include "common/log.h"

#include <android/native_window.h>
#include <cstring>
#include <mutex>
#include <string>

namespace {
constexpr const char* kLogTag = "VideoTextureBridge";

struct VideoFrame {
    std::mutex mutex;
    uint32_t width = 0;
    uint32_t height = 0;
    // RGBA pixel data (width * height * 4 bytes)
    uint8_t* rgba_data = nullptr;
    size_t rgba_size = 0;
    uint64_t frame_index = 0;
    bool has_frame = false;
};

VideoFrame g_video_frame;

}  // namespace

namespace teleop::video {

void UpdateVideoFrame(
    const uint8_t* argb_pixels,
    uint32_t width,
    uint32_t height) {
    if (!argb_pixels || width == 0 || height == 0) {
        return;
    }

    const size_t needed = static_cast<size_t>(width) * height * 4;

    std::lock_guard<std::mutex> lock(g_video_frame.mutex);

    if (g_video_frame.rgba_size < needed) {
        delete[] g_video_frame.rgba_data;
        g_video_frame.rgba_data = new uint8_t[needed];
        g_video_frame.rgba_size = needed;
        common::LogInfo(
            kLogTag,
            ("Allocated video buffer " + std::to_string(width) + "x" +
             std::to_string(height))
                .c_str());
    }

    // Convert Android ARGB_8888 (Java int = 0xAARRGGBB) -> RGBA
    const uint32_t pixel_count = width * height;
    const uint32_t* src = reinterpret_cast<const uint32_t*>(argb_pixels);
    uint8_t* dst = g_video_frame.rgba_data;
    for (uint32_t i = 0; i < pixel_count; ++i) {
        uint32_t px = src[i];
        dst[0] = (px >> 16) & 0xFF;  // R
        dst[1] = (px >> 8) & 0xFF;   // G
        dst[2] = (px >> 0) & 0xFF;   // B
        dst[3] = (px >> 24) & 0xFF;  // A
        dst += 4;
    }

    g_video_frame.width = width;
    g_video_frame.height = height;
    g_video_frame.frame_index++;
    g_video_frame.has_frame = true;
}

bool DrawVideoFrameToWindow(ANativeWindow* window) {
    if (!window) {
        return false;
    }

    std::lock_guard<std::mutex> lock(g_video_frame.mutex);
    if (!g_video_frame.has_frame || !g_video_frame.rgba_data) {
        return false;
    }

    const int32_t w = static_cast<int32_t>(g_video_frame.width);
    const int32_t h = static_cast<int32_t>(g_video_frame.height);

    ANativeWindow_setBuffersGeometry(window, w, h, WINDOW_FORMAT_RGBA_8888);

    ANativeWindow_Buffer buffer{};
    if (ANativeWindow_lock(window, &buffer, nullptr) != 0) {
        common::LogError(kLogTag, "ANativeWindow_lock failed");
        return false;
    }

    // Copy row by row (stride may differ)
    const uint8_t* src_row = g_video_frame.rgba_data;
    auto* dst_row = static_cast<uint8_t*>(buffer.bits);
    const int32_t copy_width = (buffer.width < w ? buffer.width : w);
    const int32_t copy_height = (buffer.height < h ? buffer.height : h);
    const int32_t src_stride = w * 4;
    const int32_t dst_stride = buffer.stride * 4;

    for (int32_t row = 0; row < copy_height; ++row) {
        std::memcpy(dst_row, src_row, copy_width * 4);
        src_row += src_stride;
        dst_row += dst_stride;
    }

    ANativeWindow_unlockAndPost(window);
    return true;
}

bool HasVideoFrame() {
    std::lock_guard<std::mutex> lock(g_video_frame.mutex);
    return g_video_frame.has_frame;
}

std::string DescribeTextureBridge() {
    std::lock_guard<std::mutex> lock(g_video_frame.mutex);
    if (!g_video_frame.has_frame) {
        return "video.texture_bridge=waiting-for-frame";
    }
    return "video.texture_bridge=active frame_index=" +
           std::to_string(g_video_frame.frame_index) + " " +
           std::to_string(g_video_frame.width) + "x" +
           std::to_string(g_video_frame.height);
}

}  // namespace teleop::video
