cmake_minimum_required(VERSION 3.22.1)

project("teleop")

add_library(${CMAKE_PROJECT_NAME} SHARED
    src/app/jni_entry.cpp
    src/app/app_main.cpp
    src/xr/xr_instance.cpp
    src/xr/xr_session.cpp
    src/xr/xr_frame_loop.cpp
    src/xr/xr_actions.cpp
    src/renderer/vk_context.cpp
    src/renderer/mesh_curved_screen.cpp
    src/renderer/video_pipeline.cpp
    src/renderer/hud_renderer.cpp
    src/video/video_texture_bridge.cpp
    src/video/video_timing.cpp
    src/input/pose_provider.cpp
    src/input/controller_input.cpp
    src/common/log.cpp
    src/common/time.cpp
)

target_compile_features(${CMAKE_PROJECT_NAME} PRIVATE cxx_std_17)
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
    XR_USE_PLATFORM_ANDROID
    XR_USE_GRAPHICS_API_VULKAN
)

find_library(log-lib log)
find_library(android-lib android)
find_library(vulkan-lib vulkan)
find_package(OpenXR REQUIRED CONFIG)

target_link_libraries(${CMAKE_PROJECT_NAME}
    ${android-lib}
    ${log-lib}
    ${vulkan-lib}
    OpenXR::headers
    OpenXR::openxr_loader
)
