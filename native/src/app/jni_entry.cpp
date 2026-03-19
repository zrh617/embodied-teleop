#include "app/app_runtime.h"

#include <jni.h>

extern "C" JNIEXPORT jboolean JNICALL
Java_com_xr_teleop_NativeBridge_nativeInit(JNIEnv* env, jobject thiz, jobject activity) {
    (void)thiz;
    JavaVM* vm = nullptr;
    env->GetJavaVM(&vm);
    return teleop::app::Init(vm, activity) ? JNI_TRUE : JNI_FALSE;
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeOnResume(JNIEnv* env, jobject thiz) {
    (void)env;
    (void)thiz;
    teleop::app::OnResume();
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeOnPause(JNIEnv* env, jobject thiz) {
    (void)env;
    (void)thiz;
    teleop::app::OnPause();
}

extern "C" JNIEXPORT void JNICALL
Java_com_xr_teleop_NativeBridge_nativeRequestExit(JNIEnv* env, jobject thiz) {
    (void)env;
    (void)thiz;
    teleop::app::RequestExit();
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_xr_teleop_NativeBridge_nativeGetStatus(JNIEnv* env, jobject thiz) {
    (void)thiz;
    const std::string status = teleop::app::GetStatus();
    return env->NewStringUTF(status.c_str());
}
