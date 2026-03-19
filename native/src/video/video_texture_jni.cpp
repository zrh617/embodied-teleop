#include <cstring>
#include <jni.h>
#include "common/log.h"

namespace {
constexpr const char* kLogTag = "VideoNativeBridge";

// 视频纹理缓冲区
struct VideoTextureBuffer {
    uint32_t width = 0;
    uint32_t height = 0;
    uint8_t* rgba_data = nullptr;
    
    ~VideoTextureBuffer() {
        if (rgba_data) {
            delete[] rgba_data;
            rgba_data = nullptr;
        }
    }
};

static VideoTextureBuffer g_video_buffer;
}

extern "C" {

/**
 * 从Java更新视频帧
 * 将ARGB像素数据转换为RGBA格式用于Vulkan
 */
JNIEXPORT void JNICALL Java_com_xr_teleop_NativeBridge_nativeUpdateVideoFrame(
    JNIEnv* env,
    jclass clazz,
    jintArray pixelData,
    jint width,
    jint height) {
    
    if (!pixelData || width <= 0 || height <= 0) {
        teleop::common::LogError(kLogTag, "Invalid video frame parameters");
        return;
    }

    try {
        // 获取像素数据
        int* pixels = env->GetIntArrayElements(pixelData, nullptr);
        if (!pixels) {
            teleop::common::LogError(kLogTag, "Failed to get pixel array");
            return;
        }

        size_t pixel_count = width * height;
        size_t buffer_size = pixel_count * 4;  // RGBA format

        // 分配或重新分配缓冲区
        if (!g_video_buffer.rgba_data || 
            g_video_buffer.width != width || 
            g_video_buffer.height != height) {
            
            if (g_video_buffer.rgba_data) {
                delete[] g_video_buffer.rgba_data;
            }
            
            g_video_buffer.width = width;
            g_video_buffer.height = height;
            g_video_buffer.rgba_data = new uint8_t[buffer_size];
            
            teleop::common::LogInfo(kLogTag, 
                "Allocated video buffer: " + std::to_string(width) + 
                "x" + std::to_string(height));
        }

        // 转换ARGB到RGBA
        // Java Bitmap通常使用ARGB_8888格式
        uint8_t* rgba_ptr = g_video_buffer.rgba_data;
        
        for (size_t i = 0; i < pixel_count; i++) {
            int argb = pixels[i];
            
            // 提取颜色分量（ARGB格式）
            uint8_t a = (argb >> 24) & 0xFF;  // Alpha
            uint8_t r = (argb >> 16) & 0xFF;  // Red
            uint8_t g = (argb >> 8) & 0xFF;   // Green
            uint8_t b = argb & 0xFF;           // Blue
            
            // 存储为RGBA格式
            *rgba_ptr++ = r;
            *rgba_ptr++ = g;
            *rgba_ptr++ = b;
            *rgba_ptr++ = a;
        }

        teleop::common::LogInfo(kLogTag, 
            "Video frame updated: " + std::to_string(width) + 
            "x" + std::to_string(height) + " (" + 
            std::to_string(buffer_size) + " bytes)");

        // 释放Java数组
        env->ReleaseIntArrayElements(pixelData, pixels, JNI_ABORT);

    } catch (const std::exception& e) {
        teleop::common::LogError(kLogTag, "Exception in nativeUpdateVideoFrame: " + std::string(e.what()));
    }
}

/**
 * 获取当前视频缓冲区的指针
 * 供渲染器使用
 */
JNIEXPORT jlong JNICALL Java_com_xr_teleop_NativeBridgeVideoExtension_nativeGetVideoBuffer(
    JNIEnv* env,
    jclass clazz) {
    
    return reinterpret_cast<jlong>(&g_video_buffer);
}

/**
 * 获取视频缓冲区的宽度
 */
JNIEXPORT jint JNICALL Java_com_xr_teleop_NativeBridgeVideoExtension_nativeGetVideoWidth(
    JNIEnv* env,
    jclass clazz) {
    
    return g_video_buffer.width;
}

/**
 * 获取视频缓冲区的高度
 */
JNIEXPORT jint JNICALL Java_com_xr_teleop_NativeBridgeVideoExtension_nativeGetVideoHeight(
    JNIEnv* env,
    jclass clazz) {
    
    return g_video_buffer.height;
}

/**
 * 设置应用状态（用于调试和UI反馈）
 */
JNIEXPORT void JNICALL Java_com_xr_teleop_NativeBridge_nativeSetStatus(
    JNIEnv* env,
    jclass clazz,
    jstring status) {
    
    try {
        const char* status_str = env->GetStringUTFChars(status, nullptr);
        if (status_str) {
            teleop::common::LogInfo(kLogTag, std::string("Status: ") + status_str);
            env->ReleaseStringUTFChars(status, status_str);
        }
    } catch (const std::exception& e) {
        teleop::common::LogError(kLogTag, "Exception in nativeSetStatus: " + std::string(e.what()));
    }
}

}  // extern "C"
