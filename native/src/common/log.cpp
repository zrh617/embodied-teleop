#include "common/log.h"

#include <android/log.h>

namespace teleop::common {

void LogInfo(const char* tag, const char* message) {
    __android_log_print(ANDROID_LOG_INFO, tag, "%s", message);
}

void LogError(const char* tag, const char* message) {
    __android_log_print(ANDROID_LOG_ERROR, tag, "%s", message);
}

}  // namespace teleop::common
