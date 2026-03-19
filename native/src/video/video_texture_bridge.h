#pragma once

#include <cstdint>
#include <string>

struct ANativeWindow;

namespace teleop::video {

// Called from JNI with raw ARGB_8888 pixel data from Java Bitmap.
void UpdateVideoFrame(
    const uint8_t* argb_pixels,
    uint32_t width,
    uint32_t height);

// Blit the latest video frame into an ANativeWindow (quad swapchain surface).
// Returns true if a frame was available and drawn.
bool DrawVideoFrameToWindow(ANativeWindow* window);

// Returns true if at least one frame has been received.
bool HasVideoFrame();

std::string DescribeTextureBridge();

}  // namespace teleop::video
