package com.xr.teleop.xr

import android.util.Log

/**
 * Interprets raw controller button states according to v2 spec:
 *
 * Left controller:
 *  X (primary)        → short press → CONFIRM_FOLLOW
 *  Y (secondary)      → short press → TOGGLE_RECORD
 *
 * Right controller:
 *  A (primary)        → short press → TOGGLE_LOCK
 *  B (secondary)      → short press → STOP_FOLLOW
 *                     → long press 3.5 s → START_CALIBRATION (non-following)
 *
 * System combo:
 *  left thumbstick click + right thumbstick click → SOFT_ESTOP
 */
class ButtonStateMachine {

    // ── B long/short press tracking ──────────────────────────────────────────
    private var bPressStartMs: Long = 0L
    private var bWasPressed: Boolean = false
    private var bLongPressConsumed: Boolean = false
    private var lastStopFollowMs: Long = 0L

    // ── Edge detection for single-click buttons ──────────────────────────────
    private var aWasPressed: Boolean = false
    private var xWasPressed: Boolean = false
    private var yWasPressed: Boolean = false

    // ── Soft-estop combo debounce ────────────────────────────────────────────
    private var comboWasActive: Boolean = false

    companion object {
        private const val TAG = "ButtonStateMachine"
        const val B_LONG_PRESS_MS = 3500L
        private const val B_SHORT_PRESS_MIN_MS = 40L
        private const val STOP_FOLLOW_COOLDOWN_MS = 350L
        const val GRIP_ENABLE_THRESHOLD = 0.3f
    }

    fun update(
        left: ControllerState,
        right: ControllerState,
        teleopState: TeleopState,
        nowMs: Long = System.currentTimeMillis(),
    ): List<TeleopCommandType> {
        val commands = mutableListOf<TeleopCommandType>()

        val xPressed = left.buttons.primary             // X
        val yPressed = left.buttons.secondary           // Y

        val aPressed = right.buttons.primary            // A
        val bPressed = right.buttons.secondary          // B

        val comboActive = left.buttons.thumbstickClick && right.buttons.thumbstickClick

        // ── Soft-estop combo ─────────────────────────────────────────────────
        if (comboActive && !comboWasActive) {
            Log.w(TAG, "Soft e-stop combo triggered")
            commands += TeleopCommandType.SOFT_ESTOP
        }
        comboWasActive = comboActive

        // ── Left X: confirm follow ───────────────────────────────────────────
        if (xPressed && !xWasPressed) {
            commands += TeleopCommandType.CONFIRM_FOLLOW
            Log.i(TAG, "X pressed → CONFIRM_FOLLOW")
        }
        xWasPressed = xPressed

        // ── Left Y: toggle record ────────────────────────────────────────────
        if (yPressed && !yWasPressed) {
            commands += TeleopCommandType.TOGGLE_RECORD
            Log.i(TAG, "Y pressed → TOGGLE_RECORD")
        }
        yWasPressed = yPressed

        // ── Right A: toggle lock ─────────────────────────────────────────────
        if (aPressed && !aWasPressed) {
            commands += TeleopCommandType.TOGGLE_LOCK
            Log.i(TAG, "A pressed → TOGGLE_LOCK")
        }
        aWasPressed = aPressed

        // ── Right B: short press stop / long press calibration ───────────────
        if (bPressed) {
            if (!bWasPressed) {
                bPressStartMs = nowMs
                bLongPressConsumed = false
                bWasPressed = true
            } else {
                val held = nowMs - bPressStartMs
                if (held >= B_LONG_PRESS_MS && !bLongPressConsumed) {
                    bLongPressConsumed = true
                    if (!teleopState.isFollowing()) {
                        commands += TeleopCommandType.START_CALIBRATION
                        Log.i(TAG, "B long-press → START_CALIBRATION")
                    } else {
                        Log.w(TAG, "B long-press ignored: currently following")
                    }
                }
            }
        } else if (bWasPressed) {
            val held = nowMs - bPressStartMs
            if (!bLongPressConsumed && held >= B_SHORT_PRESS_MIN_MS) {
                val sinceLastStop = nowMs - lastStopFollowMs
                if (sinceLastStop >= STOP_FOLLOW_COOLDOWN_MS) {
                    commands += TeleopCommandType.STOP_FOLLOW
                    lastStopFollowMs = nowMs
                    Log.i(TAG, "B short-press → STOP_FOLLOW")
                } else {
                    Log.d(TAG, "B short-press suppressed by cooldown")
                }
            }
            bWasPressed = false
        }

        return commands
    }

    fun isLeftGripEnabled(left: ControllerState): Boolean = left.grip >= GRIP_ENABLE_THRESHOLD
    fun isRightGripEnabled(right: ControllerState): Boolean = right.grip >= GRIP_ENABLE_THRESHOLD

    fun reset() {
        bPressStartMs = 0L
        bWasPressed = false
        bLongPressConsumed = false
        lastStopFollowMs = 0L

        aWasPressed = false
        xWasPressed = false
        yWasPressed = false
        comboWasActive = false
    }
}
