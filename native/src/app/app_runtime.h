#pragma once

#include <jni.h>
#include <string>

namespace teleop::app {

bool Init(JavaVM* vm, jobject activity);
void OnResume();
void OnPause();
void RequestExit();
std::string GetStatus();

}  // namespace teleop::app
