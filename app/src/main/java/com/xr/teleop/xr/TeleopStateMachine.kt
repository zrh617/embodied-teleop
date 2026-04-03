package com.xr.teleop.xr

import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * v2 Teleop state machine — mirrors section 6 of the design spec.
 *
 * States: IDLE → ENABLED → CALIBRATING → CALIBRATED → SYNCING
 *       → SYNC_READY → FOLLOWING ↔ RECORDING ↔ LOCKED
 *       → STOPPED / E_STOP / FAULT
 *
 * External code drives the machine via [dispatch]. The current state is
 * exposed as a [StateFlow] so the UI can observe it.
 */
enum class TeleopState {
    IDLE,
    ENABLED,
    CALIBRATING,
    CALIBRATED,
    SYNCING,
    SYNC_READY,
    FOLLOWING,
    RECORDING,
    LOCKED,
    STOPPED,
    E_STOP,
    FAULT;

    fun isFollowing(): Boolean = this == FOLLOWING || this == RECORDING || this == LOCKED
    fun canEnterFollow(): Boolean = this == SYNC_READY
    fun canCalibrate(): Boolean = this == ENABLED || this == CALIBRATED
}

class TeleopStateMachine {

    private val _state = MutableStateFlow(TeleopState.IDLE)
    val state: StateFlow<TeleopState> = _state.asStateFlow()
    val current: TeleopState get() = _state.value

    // v2: remember lock source to restore FOLLOWING/RECORDING on unlock
    private var lockReturnState: TeleopState = TeleopState.FOLLOWING

    companion object {
        private const val TAG = "TeleopFSM"
    }

    /**
     * Dispatch a command into the state machine.
     * Returns true if the transition was accepted, false if rejected.
     */
    fun dispatch(cmd: TeleopCommandType): Boolean {
        val from = current
        val to: TeleopState? = when (cmd) {
            TeleopCommandType.ENABLE -> when (from) {
                TeleopState.IDLE, TeleopState.STOPPED -> TeleopState.ENABLED
                else -> null
            }
            TeleopCommandType.DISABLE -> when (from) {
                TeleopState.ENABLED, TeleopState.STOPPED -> TeleopState.IDLE
                else -> null
            }
            TeleopCommandType.START_CALIBRATION -> when {
                from.canCalibrate() -> TeleopState.CALIBRATING
                else -> null
            }
            TeleopCommandType.FINISH_CALIBRATION -> when (from) {
                TeleopState.CALIBRATING -> TeleopState.CALIBRATED
                else -> null
            }
            TeleopCommandType.START_SYNC -> when (from) {
                TeleopState.CALIBRATED -> TeleopState.SYNCING
                else -> null
            }
            TeleopCommandType.CONFIRM_FOLLOW -> when (from) {
                TeleopState.SYNC_READY -> TeleopState.FOLLOWING
                else -> null
            }
            TeleopCommandType.TOGGLE_RECORD -> when (from) {
                TeleopState.FOLLOWING -> TeleopState.RECORDING
                TeleopState.RECORDING -> TeleopState.FOLLOWING
                else -> null
            }
            TeleopCommandType.TOGGLE_LOCK -> when (from) {
                TeleopState.FOLLOWING -> {
                    lockReturnState = TeleopState.FOLLOWING
                    TeleopState.LOCKED
                }
                TeleopState.RECORDING -> {
                    lockReturnState = TeleopState.RECORDING
                    TeleopState.LOCKED
                }
                TeleopState.LOCKED -> lockReturnState
                else -> null
            }
            TeleopCommandType.STOP_FOLLOW -> when {
                from.isFollowing() || from == TeleopState.SYNC_READY -> TeleopState.STOPPED
                else -> null
            }
            TeleopCommandType.SOFT_ESTOP -> when (from) {
                TeleopState.IDLE, TeleopState.FAULT -> null  // already safe
                else -> TeleopState.E_STOP
            }
            TeleopCommandType.CLEAR_ESTOP -> when (from) {
                TeleopState.E_STOP -> TeleopState.ENABLED
                else -> null
            }
            TeleopCommandType.NONE -> null
        }

        return if (to != null) {
            Log.i(TAG, "$from --[${cmd.name}]--> $to")
            _state.value = to
            true
        } else {
            Log.w(TAG, "$from --[${cmd.name}]--> REJECTED")
            false
        }
    }

    /** Called when robot confirms sync is complete. */
    fun onSyncComplete() {
        if (current == TeleopState.SYNCING) {
            Log.i(TAG, "Sync complete → SYNC_READY")
            _state.value = TeleopState.SYNC_READY
        }
    }

    /** Called when calibration completes (e.g. 5 s timer fires). */
    fun onCalibrationComplete() {
        dispatch(TeleopCommandType.FINISH_CALIBRATION)
    }

    /** Force fault state (e.g. tracking lost, comms timeout). */
    fun onFault(reason: String) {
        Log.e(TAG, "FAULT: $reason")
        _state.value = TeleopState.FAULT
    }

    fun reset() {
        lockReturnState = TeleopState.FOLLOWING
        _state.value = TeleopState.IDLE
    }
}
