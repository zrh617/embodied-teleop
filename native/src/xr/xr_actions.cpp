#include "xr/xr_runtime.h"

#include <cstdio>
#include <sstream>
#include <string>

namespace {

constexpr const char* kActionSetName = "teleop_actions";
constexpr const char* kActionSetLocalizedName = "Teleop Actions";
constexpr const char* kHandPoseActionName = "hand_pose";
constexpr const char* kHandPoseActionLocalizedName = "Hand Pose";

bool CheckXr(XrInstance instance, XrResult result, const char* step, std::string* error) {
    if (XR_SUCCEEDED(result)) {
        return true;
    }

    if (error != nullptr) {
        char buffer[XR_MAX_RESULT_STRING_SIZE];
        buffer[0] = '\0';
        if (instance != XR_NULL_HANDLE) {
            xrResultToString(instance, result, buffer);
            *error = std::string(step) + " failed with " + buffer;
        } else {
            *error = std::string(step) + " failed with " + std::to_string(result);
        }
    }
    return false;
}

}  // namespace

namespace teleop::xr {

bool CreateActions(Runtime* runtime, std::string* error) {
    if (runtime == nullptr || runtime->instance == XR_NULL_HANDLE || runtime->session == XR_NULL_HANDLE) {
        if (error != nullptr) {
            *error = "CreateActions called before OpenXR instance/session is ready";
        }
        return false;
    }

    XrActionSetCreateInfo action_set_info{XR_TYPE_ACTION_SET_CREATE_INFO};
    std::snprintf(action_set_info.actionSetName, XR_MAX_ACTION_SET_NAME_SIZE, "%s", kActionSetName);
    std::snprintf(
        action_set_info.localizedActionSetName,
        XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE,
        "%s",
        kActionSetLocalizedName);
    action_set_info.priority = 0;

    if (!CheckXr(
            runtime->instance,
            xrCreateActionSet(runtime->instance, &action_set_info, &runtime->action_set),
            "xrCreateActionSet",
            error)) {
        return false;
    }

    if (!CheckXr(
            runtime->instance,
            xrStringToPath(runtime->instance, "/user/hand/left", &runtime->left_hand_path),
            "xrStringToPath(/user/hand/left)",
            error) ||
        !CheckXr(
            runtime->instance,
            xrStringToPath(runtime->instance, "/user/hand/right", &runtime->right_hand_path),
            "xrStringToPath(/user/hand/right)",
            error)) {
        return false;
    }

    XrActionCreateInfo action_info{XR_TYPE_ACTION_CREATE_INFO};
    action_info.actionType = XR_ACTION_TYPE_POSE_INPUT;
    std::snprintf(action_info.actionName, XR_MAX_ACTION_NAME_SIZE, "%s", kHandPoseActionName);
    std::snprintf(
        action_info.localizedActionName,
        XR_MAX_LOCALIZED_ACTION_NAME_SIZE,
        "%s",
        kHandPoseActionLocalizedName);

    const XrPath hand_subaction_paths[2] = {
        runtime->left_hand_path,
        runtime->right_hand_path,
    };
    action_info.countSubactionPaths = 2;
    action_info.subactionPaths = hand_subaction_paths;

    if (!CheckXr(
            runtime->instance,
            xrCreateAction(runtime->action_set, &action_info, &runtime->hand_pose_action),
            "xrCreateAction",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    XrPath simple_profile_path = XR_NULL_PATH;
    XrPath left_grip_pose_path = XR_NULL_PATH;
    XrPath right_grip_pose_path = XR_NULL_PATH;

    if (!CheckXr(
            runtime->instance,
            xrStringToPath(runtime->instance, "/interaction_profiles/khr/simple_controller", &simple_profile_path),
            "xrStringToPath(simple_controller)",
            error) ||
        !CheckXr(
            runtime->instance,
            xrStringToPath(runtime->instance, "/user/hand/left/input/grip/pose", &left_grip_pose_path),
            "xrStringToPath(left_grip_pose)",
            error) ||
        !CheckXr(
            runtime->instance,
            xrStringToPath(runtime->instance, "/user/hand/right/input/grip/pose", &right_grip_pose_path),
            "xrStringToPath(right_grip_pose)",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    XrActionSuggestedBinding bindings[2] = {
        {runtime->hand_pose_action, left_grip_pose_path},
        {runtime->hand_pose_action, right_grip_pose_path},
    };

    XrInteractionProfileSuggestedBinding suggested_bindings{
        XR_TYPE_INTERACTION_PROFILE_SUGGESTED_BINDING};
    suggested_bindings.interactionProfile = simple_profile_path;
    suggested_bindings.countSuggestedBindings = 2;
    suggested_bindings.suggestedBindings = bindings;

    if (!CheckXr(
            runtime->instance,
            xrSuggestInteractionProfileBindings(runtime->instance, &suggested_bindings),
            "xrSuggestInteractionProfileBindings",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    XrSessionActionSetsAttachInfo attach_info{XR_TYPE_SESSION_ACTION_SETS_ATTACH_INFO};
    attach_info.countActionSets = 1;
    attach_info.actionSets = &runtime->action_set;

    if (!CheckXr(
            runtime->instance,
            xrAttachSessionActionSets(runtime->session, &attach_info),
            "xrAttachSessionActionSets",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    XrActionSpaceCreateInfo left_space_info{XR_TYPE_ACTION_SPACE_CREATE_INFO};
    left_space_info.action = runtime->hand_pose_action;
    left_space_info.subactionPath = runtime->left_hand_path;
    left_space_info.poseInActionSpace.orientation.w = 1.0f;

    if (!CheckXr(
            runtime->instance,
            xrCreateActionSpace(runtime->session, &left_space_info, &runtime->left_hand_space),
            "xrCreateActionSpace(left)",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    XrActionSpaceCreateInfo right_space_info{XR_TYPE_ACTION_SPACE_CREATE_INFO};
    right_space_info.action = runtime->hand_pose_action;
    right_space_info.subactionPath = runtime->right_hand_path;
    right_space_info.poseInActionSpace.orientation.w = 1.0f;

    if (!CheckXr(
            runtime->instance,
            xrCreateActionSpace(runtime->session, &right_space_info, &runtime->right_hand_space),
            "xrCreateActionSpace(right)",
            error)) {
        DestroyActions(runtime);
        return false;
    }

    runtime->actions_ready = true;
    runtime->left_hand_active = false;
    runtime->right_hand_active = false;
    runtime->left_hand_pose = {};
    runtime->right_hand_pose = {};
    return true;
}

void DestroyActions(Runtime* runtime) {
    if (runtime == nullptr) {
        return;
    }

    if (runtime->left_hand_space != XR_NULL_HANDLE) {
        xrDestroySpace(runtime->left_hand_space);
        runtime->left_hand_space = XR_NULL_HANDLE;
    }
    if (runtime->right_hand_space != XR_NULL_HANDLE) {
        xrDestroySpace(runtime->right_hand_space);
        runtime->right_hand_space = XR_NULL_HANDLE;
    }
    if (runtime->hand_pose_action != XR_NULL_HANDLE) {
        xrDestroyAction(runtime->hand_pose_action);
        runtime->hand_pose_action = XR_NULL_HANDLE;
    }
    if (runtime->action_set != XR_NULL_HANDLE) {
        xrDestroyActionSet(runtime->action_set);
        runtime->action_set = XR_NULL_HANDLE;
    }

    runtime->actions_ready = false;
    runtime->left_hand_active = false;
    runtime->right_hand_active = false;
    runtime->left_hand_pose = {};
    runtime->right_hand_pose = {};
}

bool UpdateHandPoses(Runtime* runtime, XrTime display_time, std::string* error) {
    if (runtime == nullptr || !runtime->actions_ready || runtime->session == XR_NULL_HANDLE ||
        runtime->app_space == XR_NULL_HANDLE) {
        return true;
    }

    XrActiveActionSet active_action_set{};
    active_action_set.actionSet = runtime->action_set;

    XrActionsSyncInfo sync_info{XR_TYPE_ACTIONS_SYNC_INFO};
    sync_info.countActiveActionSets = 1;
    sync_info.activeActionSets = &active_action_set;

    if (!CheckXr(runtime->instance, xrSyncActions(runtime->session, &sync_info), "xrSyncActions", error)) {
        return false;
    }

    XrActionStateGetInfo left_state_info{XR_TYPE_ACTION_STATE_GET_INFO};
    left_state_info.action = runtime->hand_pose_action;
    left_state_info.subactionPath = runtime->left_hand_path;
    XrActionStatePose left_state{XR_TYPE_ACTION_STATE_POSE};
    if (!CheckXr(
            runtime->instance,
            xrGetActionStatePose(runtime->session, &left_state_info, &left_state),
            "xrGetActionStatePose(left)",
            error)) {
        return false;
    }

    XrActionStateGetInfo right_state_info{XR_TYPE_ACTION_STATE_GET_INFO};
    right_state_info.action = runtime->hand_pose_action;
    right_state_info.subactionPath = runtime->right_hand_path;
    XrActionStatePose right_state{XR_TYPE_ACTION_STATE_POSE};
    if (!CheckXr(
            runtime->instance,
            xrGetActionStatePose(runtime->session, &right_state_info, &right_state),
            "xrGetActionStatePose(right)",
            error)) {
        return false;
    }

    bool left_active = false;
    bool right_active = false;
    XrPosef left_pose{};
    XrPosef right_pose{};

    if (left_state.isActive && runtime->left_hand_space != XR_NULL_HANDLE) {
        XrSpaceLocation left_location{XR_TYPE_SPACE_LOCATION};
        if (!CheckXr(
                runtime->instance,
                xrLocateSpace(runtime->left_hand_space, runtime->app_space, display_time, &left_location),
                "xrLocateSpace(left)",
                error)) {
            return false;
        }
        const XrSpaceLocationFlags required_flags =
            XR_SPACE_LOCATION_POSITION_VALID_BIT | XR_SPACE_LOCATION_ORIENTATION_VALID_BIT;
        left_active = (left_location.locationFlags & required_flags) == required_flags;
        if (left_active) {
            left_pose = left_location.pose;
        }
    }

    if (right_state.isActive && runtime->right_hand_space != XR_NULL_HANDLE) {
        XrSpaceLocation right_location{XR_TYPE_SPACE_LOCATION};
        if (!CheckXr(
                runtime->instance,
                xrLocateSpace(runtime->right_hand_space, runtime->app_space, display_time, &right_location),
                "xrLocateSpace(right)",
                error)) {
            return false;
        }
        const XrSpaceLocationFlags required_flags =
            XR_SPACE_LOCATION_POSITION_VALID_BIT | XR_SPACE_LOCATION_ORIENTATION_VALID_BIT;
        right_active = (right_location.locationFlags & required_flags) == required_flags;
        if (right_active) {
            right_pose = right_location.pose;
        }
    }

    runtime->left_hand_active = left_active;
    runtime->right_hand_active = right_active;
    runtime->left_hand_pose = left_pose;
    runtime->right_hand_pose = right_pose;

    return true;
}

std::string DescribeActions(const Runtime* runtime) {
    if (runtime == nullptr) {
        return "xr.actions=runtime-null";
    }

    std::ostringstream stream;
    stream << "xr.actions=" << (runtime->actions_ready ? "ready" : "not-ready")
           << " left.active=" << (runtime->left_hand_active ? "true" : "false")
           << " right.active=" << (runtime->right_hand_active ? "true" : "false");
    return stream.str();
}

}  // namespace teleop::xr
