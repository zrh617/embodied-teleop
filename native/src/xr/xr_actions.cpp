#include "xr/xr_runtime.h"

#include <cstdio>
#include <sstream>
#include <string>

namespace {

constexpr const char* kActionSetName = "teleop_actions";
constexpr const char* kActionSetLocalizedName = "Teleop Actions";

bool CheckXr(XrInstance instance, XrResult result, const char* step, std::string* error) {
    if (XR_SUCCEEDED(result)) return true;
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

bool CreateFloatAction(XrInstance inst, XrActionSet aset, const char* name,
                       const char* loc, uint32_t n, const XrPath* paths,
                       XrAction* out, std::string* err) {
    XrActionCreateInfo i{XR_TYPE_ACTION_CREATE_INFO};
    i.actionType = XR_ACTION_TYPE_FLOAT_INPUT;
    std::snprintf(i.actionName, XR_MAX_ACTION_NAME_SIZE, "%s", name);
    std::snprintf(i.localizedActionName, XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE, "%s", loc);
    i.countSubactionPaths = n; i.subactionPaths = paths;
    return CheckXr(inst, xrCreateAction(aset, &i, out), name, err);
}

bool CreateBoolAction(XrInstance inst, XrActionSet aset, const char* name,
                      const char* loc, uint32_t n, const XrPath* paths,
                      XrAction* out, std::string* err) {
    XrActionCreateInfo i{XR_TYPE_ACTION_CREATE_INFO};
    i.actionType = XR_ACTION_TYPE_BOOLEAN_INPUT;
    std::snprintf(i.actionName, XR_MAX_ACTION_NAME_SIZE, "%s", name);
    std::snprintf(i.localizedActionName, XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE, "%s", loc);
    i.countSubactionPaths = n; i.subactionPaths = paths;
    return CheckXr(inst, xrCreateAction(aset, &i, out), name, err);
}

bool CreateVec2Action(XrInstance inst, XrActionSet aset, const char* name,
                      const char* loc, uint32_t n, const XrPath* paths,
                      XrAction* out, std::string* err) {
    XrActionCreateInfo i{XR_TYPE_ACTION_CREATE_INFO};
    i.actionType = XR_ACTION_TYPE_VECTOR2F_INPUT;
    std::snprintf(i.actionName, XR_MAX_ACTION_NAME_SIZE, "%s", name);
    std::snprintf(i.localizedActionName, XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE, "%s", loc);
    i.countSubactionPaths = n; i.subactionPaths = paths;
    return CheckXr(inst, xrCreateAction(aset, &i, out), name, err);
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

    // ── Action set ────────────────────────────────────────────────────────────
    XrActionSetCreateInfo action_set_info{XR_TYPE_ACTION_SET_CREATE_INFO};
    std::snprintf(action_set_info.actionSetName, XR_MAX_ACTION_SET_NAME_SIZE, "%s", kActionSetName);
    std::snprintf(action_set_info.localizedActionSetName, XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE, "%s", kActionSetLocalizedName);
    action_set_info.priority = 0;
    if (!CheckXr(runtime->instance, xrCreateActionSet(runtime->instance, &action_set_info, &runtime->action_set), "xrCreateActionSet", error)) {
        return false;
    }

    // ── Subaction paths ───────────────────────────────────────────────────────
    if (!CheckXr(runtime->instance, xrStringToPath(runtime->instance, "/user/hand/left",  &runtime->left_hand_path),  "xrStringToPath(left)",  error) ||
        !CheckXr(runtime->instance, xrStringToPath(runtime->instance, "/user/hand/right", &runtime->right_hand_path), "xrStringToPath(right)", error)) {
        DestroyActions(runtime);
        return false;
    }
    const XrPath both[2] = {runtime->left_hand_path, runtime->right_hand_path};

    // ── Pose action ───────────────────────────────────────────────────────────
    {
        XrActionCreateInfo ai{XR_TYPE_ACTION_CREATE_INFO};
        ai.actionType = XR_ACTION_TYPE_POSE_INPUT;
        std::snprintf(ai.actionName, XR_MAX_ACTION_NAME_SIZE, "hand_pose");
        std::snprintf(ai.localizedActionName, XR_MAX_LOCALIZED_ACTION_SET_NAME_SIZE, "Hand Pose");
        ai.countSubactionPaths = 2; ai.subactionPaths = both;
        if (!CheckXr(runtime->instance, xrCreateAction(runtime->action_set, &ai, &runtime->hand_pose_action), "xrCreateAction(hand_pose)", error)) {
            DestroyActions(runtime); return false;
        }
    }
    // ── Trigger ───────────────────────────────────────────────────────────────
    if (!CreateFloatAction(runtime->instance, runtime->action_set, "trigger", "Trigger", 2, both, &runtime->trigger_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── Squeeze ───────────────────────────────────────────────────────────────
    if (!CreateFloatAction(runtime->instance, runtime->action_set, "squeeze", "Squeeze", 2, both, &runtime->squeeze_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── Thumbstick (vec2) ─────────────────────────────────────────────────────
    if (!CreateVec2Action(runtime->instance, runtime->action_set, "thumbstick", "Thumbstick", 2, both, &runtime->thumbstick_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── Thumbstick click ──────────────────────────────────────────────────────
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "thumbstick_click", "Thumbstick Click", 2, both, &runtime->thumbstick_click_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── A / B (right only) ────────────────────────────────────────────────────
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "button_a", "Button A", 1, &runtime->right_hand_path, &runtime->button_a_action, error)) {
        DestroyActions(runtime); return false;
    }
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "button_b", "Button B", 1, &runtime->right_hand_path, &runtime->button_b_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── X / Y (left only) ────────────────────────────────────────────────────
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "button_x", "Button X", 1, &runtime->left_hand_path, &runtime->button_x_action, error)) {
        DestroyActions(runtime); return false;
    }
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "button_y", "Button Y", 1, &runtime->left_hand_path, &runtime->button_y_action, error)) {
        DestroyActions(runtime); return false;
    }
    // ── Menu (left only) ─────────────────────────────────────────────────────
    if (!CreateBoolAction(runtime->instance, runtime->action_set, "menu", "Menu", 1, &runtime->left_hand_path, &runtime->menu_action, error)) {
        DestroyActions(runtime); return false;
    }

    // ── Interaction profile: Oculus Touch Controller ──────────────────────────
    XrPath touch_profile = XR_NULL_PATH;
    if (!CheckXr(runtime->instance, xrStringToPath(runtime->instance, "/interaction_profiles/oculus/touch_controller", &touch_profile), "xrStringToPath(touch_controller)", error)) {
        DestroyActions(runtime); return false;
    }

    auto ToPath = [&](const char* s, XrPath* out) -> bool {
        return CheckXr(runtime->instance, xrStringToPath(runtime->instance, s, out), s, error);
    };
    XrPath lg, rg, lt, rt, ls, rs, lts, rts, ltc, rtc, ra, rb, lx, ly, lm;
    if (!ToPath("/user/hand/left/input/grip/pose",           &lg)  ||
        !ToPath("/user/hand/right/input/grip/pose",          &rg)  ||
        !ToPath("/user/hand/left/input/trigger/value",       &lt)  ||
        !ToPath("/user/hand/right/input/trigger/value",      &rt)  ||
        !ToPath("/user/hand/left/input/squeeze/value",       &ls)  ||
        !ToPath("/user/hand/right/input/squeeze/value",      &rs)  ||
        !ToPath("/user/hand/left/input/thumbstick",          &lts) ||
        !ToPath("/user/hand/right/input/thumbstick",         &rts) ||
        !ToPath("/user/hand/left/input/thumbstick/click",    &ltc) ||
        !ToPath("/user/hand/right/input/thumbstick/click",   &rtc) ||
        !ToPath("/user/hand/right/input/a/click",            &ra)  ||
        !ToPath("/user/hand/right/input/b/click",            &rb)  ||
        !ToPath("/user/hand/left/input/x/click",             &lx)  ||
        !ToPath("/user/hand/left/input/y/click",             &ly)  ||
        !ToPath("/user/hand/left/input/menu/click",          &lm)) {
        DestroyActions(runtime); return false;
    }

    XrActionSuggestedBinding bindings[] = {
        {runtime->hand_pose_action,        lg},
        {runtime->hand_pose_action,        rg},
        {runtime->trigger_action,          lt},
        {runtime->trigger_action,          rt},
        {runtime->squeeze_action,          ls},
        {runtime->squeeze_action,          rs},
        {runtime->thumbstick_action,       lts},
        {runtime->thumbstick_action,       rts},
        {runtime->thumbstick_click_action, ltc},
        {runtime->thumbstick_click_action, rtc},
        {runtime->button_a_action,         ra},
        {runtime->button_b_action,         rb},
        {runtime->button_x_action,         lx},
        {runtime->button_y_action,         ly},
        {runtime->menu_action,             lm},
    };
    XrInteractionProfileSuggestedBinding suggested{XR_TYPE_INTERACTION_PROFILE_SUGGESTED_BINDING};
    suggested.interactionProfile = touch_profile;
    suggested.countSuggestedBindings = static_cast<uint32_t>(sizeof(bindings) / sizeof(bindings[0]));
    suggested.suggestedBindings = bindings;
    if (!CheckXr(runtime->instance, xrSuggestInteractionProfileBindings(runtime->instance, &suggested), "xrSuggestInteractionProfileBindings", error)) {
        DestroyActions(runtime); return false;
    }

    // ── Attach ────────────────────────────────────────────────────────────────
    XrSessionActionSetsAttachInfo attach_info{XR_TYPE_SESSION_ACTION_SETS_ATTACH_INFO};
    attach_info.countActionSets = 1;
    attach_info.actionSets = &runtime->action_set;
    if (!CheckXr(runtime->instance, xrAttachSessionActionSets(runtime->session, &attach_info), "xrAttachSessionActionSets", error)) {
        DestroyActions(runtime); return false;
    }

    // ── Action spaces ─────────────────────────────────────────────────────────
    XrActionSpaceCreateInfo lsi{XR_TYPE_ACTION_SPACE_CREATE_INFO};
    lsi.action = runtime->hand_pose_action;
    lsi.subactionPath = runtime->left_hand_path;
    lsi.poseInActionSpace.orientation.w = 1.0f;
    if (!CheckXr(runtime->instance, xrCreateActionSpace(runtime->session, &lsi, &runtime->left_hand_space), "xrCreateActionSpace(left)", error)) {
        DestroyActions(runtime); return false;
    }
    XrActionSpaceCreateInfo rsi{XR_TYPE_ACTION_SPACE_CREATE_INFO};
    rsi.action = runtime->hand_pose_action;
    rsi.subactionPath = runtime->right_hand_path;
    rsi.poseInActionSpace.orientation.w = 1.0f;
    if (!CheckXr(runtime->instance, xrCreateActionSpace(runtime->session, &rsi, &runtime->right_hand_space), "xrCreateActionSpace(right)", error)) {
        DestroyActions(runtime); return false;
    }

    runtime->actions_ready = true;
    runtime->left_hand_active = false;
    runtime->right_hand_active = false;
    runtime->left_hand_pose = {};
    runtime->right_hand_pose = {};
    return true;
}

void DestroyActions(Runtime* runtime) {
    if (runtime == nullptr) return;

    auto DS = [](XrSpace& s)  { if (s != XR_NULL_HANDLE) { xrDestroySpace(s);     s = XR_NULL_HANDLE; } };
    auto DA = [](XrAction& a) { if (a != XR_NULL_HANDLE) { xrDestroyAction(a);    a = XR_NULL_HANDLE; } };

    DS(runtime->left_hand_space);
    DS(runtime->right_hand_space);
    DA(runtime->hand_pose_action);
    DA(runtime->trigger_action);
    DA(runtime->squeeze_action);
    DA(runtime->thumbstick_action);
    DA(runtime->thumbstick_click_action);
    DA(runtime->button_a_action);
    DA(runtime->button_b_action);
    DA(runtime->button_x_action);
    DA(runtime->button_y_action);
    DA(runtime->menu_action);

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

    // Helper: read float action value for a subaction path
    auto GetFloat = [&](XrAction action, XrPath subpath) -> float {
        if (action == XR_NULL_HANDLE) return 0.f;
        XrActionStateGetInfo gi{XR_TYPE_ACTION_STATE_GET_INFO};
        gi.action = action; gi.subactionPath = subpath;
        XrActionStateFloat s{XR_TYPE_ACTION_STATE_FLOAT};
        xrGetActionStateFloat(runtime->session, &gi, &s);
        return s.isActive ? s.currentState : 0.f;
    };
    auto GetBool = [&](XrAction action, XrPath subpath) -> bool {
        if (action == XR_NULL_HANDLE) return false;
        XrActionStateGetInfo gi{XR_TYPE_ACTION_STATE_GET_INFO};
        gi.action = action; gi.subactionPath = subpath;
        XrActionStateBoolean s{XR_TYPE_ACTION_STATE_BOOLEAN};
        xrGetActionStateBoolean(runtime->session, &gi, &s);
        return s.isActive && s.currentState;
    };
    auto GetVec2 = [&](XrAction action, XrPath subpath, float& ox, float& oy) {
        if (action == XR_NULL_HANDLE) { ox = oy = 0.f; return; }
        XrActionStateGetInfo gi{XR_TYPE_ACTION_STATE_GET_INFO};
        gi.action = action; gi.subactionPath = subpath;
        XrActionStateVector2f s{XR_TYPE_ACTION_STATE_VECTOR2F};
        xrGetActionStateVector2f(runtime->session, &gi, &s);
        ox = s.isActive ? s.currentState.x : 0.f;
        oy = s.isActive ? s.currentState.y : 0.f;
    };

    // ── Analog / button state ─────────────────────────────────────────────────
    runtime->left_trigger  = GetFloat(runtime->trigger_action,  runtime->left_hand_path);
    runtime->right_trigger = GetFloat(runtime->trigger_action,  runtime->right_hand_path);
    runtime->left_squeeze  = GetFloat(runtime->squeeze_action,  runtime->left_hand_path);
    runtime->right_squeeze = GetFloat(runtime->squeeze_action,  runtime->right_hand_path);
    GetVec2(runtime->thumbstick_action, runtime->left_hand_path,
            runtime->left_thumbstick_x,  runtime->left_thumbstick_y);
    GetVec2(runtime->thumbstick_action, runtime->right_hand_path,
            runtime->right_thumbstick_x, runtime->right_thumbstick_y);
    runtime->left_thumbstick_click  = GetBool(runtime->thumbstick_click_action, runtime->left_hand_path);
    runtime->right_thumbstick_click = GetBool(runtime->thumbstick_click_action, runtime->right_hand_path);
    runtime->button_a    = GetBool(runtime->button_a_action, runtime->right_hand_path);
    runtime->button_b    = GetBool(runtime->button_b_action, runtime->right_hand_path);
    runtime->button_x    = GetBool(runtime->button_x_action, runtime->left_hand_path);
    runtime->button_y    = GetBool(runtime->button_y_action, runtime->left_hand_path);
    runtime->button_menu = GetBool(runtime->menu_action,     runtime->left_hand_path);

    // ── Pose state ────────────────────────────────────────────────────────────
    auto GetPose = [&](XrAction action, XrPath subpath, XrSpace space,
                       bool& active_out, XrPosef& pose_out) {
        XrActionStateGetInfo gi{XR_TYPE_ACTION_STATE_GET_INFO};
        gi.action = action; gi.subactionPath = subpath;
        XrActionStatePose sp{XR_TYPE_ACTION_STATE_POSE};
        xrGetActionStatePose(runtime->session, &gi, &sp);
        active_out = false;
        if (sp.isActive && space != XR_NULL_HANDLE) {
            XrSpaceLocation loc{XR_TYPE_SPACE_LOCATION};
            if (XR_SUCCEEDED(xrLocateSpace(space, runtime->app_space, display_time, &loc))) {
                const XrSpaceLocationFlags req =
                    XR_SPACE_LOCATION_POSITION_VALID_BIT | XR_SPACE_LOCATION_ORIENTATION_VALID_BIT;
                if ((loc.locationFlags & req) == req) {
                    active_out = true;
                    pose_out   = loc.pose;
                }
            }
        }
    };

    GetPose(runtime->hand_pose_action, runtime->left_hand_path,
            runtime->left_hand_space, runtime->left_hand_active, runtime->left_hand_pose);
    GetPose(runtime->hand_pose_action, runtime->right_hand_path,
            runtime->right_hand_space, runtime->right_hand_active, runtime->right_hand_pose);

    return true;
}

std::string DescribeActions(const Runtime* runtime) {
    if (runtime == nullptr) return "xr.actions=runtime-null";
    std::ostringstream s;
    s << "xr.actions=" << (runtime->actions_ready ? "ready" : "not-ready")
      << " L.active=" << runtime->left_hand_active
      << " R.active=" << runtime->right_hand_active
      << " R.trig=" << runtime->right_trigger
      << " R.sqz=" << runtime->right_squeeze
      << " R.A=" << runtime->button_a
      << " R.B=" << runtime->button_b;
    return s.str();
}

}  // namespace teleop::xr
