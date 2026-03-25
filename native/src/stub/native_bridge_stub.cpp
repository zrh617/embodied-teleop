#include <jni.h>
#include <android/log.h>
#include <cstdio>

namespace {

constexpr const char* kTag = "teleop_stub";
bool g_initialized = false;
bool g_resumed = false;
int g_last_width = 0;
int g_last_height = 0;

void LogInfo(const char* message) {
    __android_log_print(ANDROID_LOG_INFO, kTag, "%s", message);
}

jstring MakeStatusString(JNIEnv* env) {
    char buffer[128];
    std::snprintf(
        buffer,
        sizeof(buffer),
        "initialized=%s,resumed=%s,last_frame=%dx%d",
        g_initialized ? "true" : "false",
        g_resumed ? "true" : "false",
        g_last_width,
        g_last_height);
    return env->NewStringUTF(buffer);
}

}  // namespace

extern "C" JNIEXPORT jboolean JNICALL
Java_com_xr_teleop_NativeBridge_nativeInit(JNIEnv*, jobject, jobject) {
    g_initialized = true;
    LogInfo("nativeInit");
    return JNI_TRUE;
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeOnResume(JNIEnv*, jobject) {
    g_resumed = true;
    LogInfo("nativeOnResume");
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeOnPause(JNIEnv*, jobject) {
    g_resumed = false;
    LogInfo("nativeOnPause");
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeRequestExit(JNIEnv*, jobject) {
    g_resumed = false;
    g_initialized = false;
    LogInfo("nativeRequestExit");
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_xr_teleop_NativeBridge_nativeGetStatus(JNIEnv* env, jobject) {
    return MakeStatusString(env);
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeUpdateVideoFrame(
    JNIEnv*,
    jobject,
    jintArray,
    jint width,
    jint height) {
    g_last_width = width;
    g_last_height = height;
    __android_log_print(
        ANDROID_LOG_VERBOSE,
        kTag,
        "nativeUpdateVideoFrame %dx%d",
        g_last_width,
        g_last_height);
}
