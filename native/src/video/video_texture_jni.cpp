#include "video/video_texture_bridge.h"

#include "common/log.h"

#include <jni.h>

namespace {
constexpr const char* kLogTag = "VideoNativeBridge";
}

extern "C" {

// Called from Kotlin: NativeBridge.nativeUpdateVideoFrame(pixels, width, height)
JNIEXPORT void JNICALL Java_com_xr_teleop_NativeBridge_nativeUpdateVideoFrame(
    JNIEnv* env,
    jobject /*thiz*/,
    jintArray pixelData,
    jint width,
    jint height) {
    if (!pixelData || width <= 0 || height <= 0) {
        teleop::common::LogError(kLogTag, "Invalid video frame parameters");
        return;
    }

    jint* pixels = env->GetIntArrayElements(pixelData, nullptr);
    if (!pixels) {
        teleop::common::LogError(kLogTag, "Failed to get pixel array elements");
        return;
    }

    teleop::video::UpdateVideoFrame(
        reinterpret_cast<const uint8_t*>(pixels),
        static_cast<uint32_t>(width),
        static_cast<uint32_t>(height));

    env->ReleaseIntArrayElements(pixelData, pixels, JNI_ABORT);
}

}  // extern "C"
