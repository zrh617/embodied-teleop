package com.xr.teleop

import android.app.Activity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.WindowManager
import com.xr.teleop.video.VideoTextureManager
import com.xr.teleop.xr.ButtonStateMachine
import com.xr.teleop.xr.TeleopCommand
import com.xr.teleop.xr.TeleopCommandType
import com.xr.teleop.xr.TeleopState
import com.xr.teleop.xr.TeleopStateMachine
import com.xr.teleop.xr.XrWsClient
import com.xr.teleop.xr.createTestXrControllerState
import com.xr.teleop.xr.parseXrControllerStateJson

class XRActivity : Activity() {

    private var nativeInitialized = false
    private var videoManager: VideoTextureManager? = null
    private var xrWsClient: XrWsClient? = null

    // v2: state machine + button interpreter
    private val teleopFsm = TeleopStateMachine()
    private val buttonFsm = ButtonStateMachine()

    // Calibration: B long-press starts, then 5 s timer emits FINISH_CALIBRATION
    private val calibHandler = Handler(Looper.getMainLooper())
    private val calibFinishRunnable = Runnable {
        Log.i(TAG, "Calibration 5 s timer done → FINISH_CALIBRATION")
        val accepted = teleopFsm.dispatch(TeleopCommandType.FINISH_CALIBRATION)
        if (accepted) {
            sendCommand(TeleopCommandType.FINISH_CALIBRATION)
        }
    }

    private val stateSenderHandler = Handler(Looper.getMainLooper())
    private var cmdSeq = 0L

    private val stateSender = object : Runnable {
        override fun run() {
            try {
                val rawJson = NativeBridge.nativeGetControllerStateJson()
                val state = try {
                    parseXrControllerStateJson(rawJson)
                } catch (e: Exception) {
                    Log.w(TAG, "Fallback to test state", e)
                    createTestXrControllerState()
                }

                val right = state.right
                val nowMs = System.currentTimeMillis()

                // ── Button state machine → dispatch commands ─────────────────
                val cmds = buttonFsm.update(
                    left = state.left,
                    right = right,
                    teleopState = teleopFsm.current,
                    nowMs = nowMs,
                )
                cmds.forEach { cmdType ->
                    teleopFsm.dispatch(cmdType)
                    sendCommand(cmdType)

                    // When calibration starts, arm the 5-second finish timer
                    if (cmdType == TeleopCommandType.START_CALIBRATION) {
                        calibHandler.removeCallbacks(calibFinishRunnable)
                        calibHandler.postDelayed(
                            calibFinishRunnable,
                            ButtonStateMachine.B_LONG_PRESS_MS,
                        )
                        Log.i(TAG, "Calibration started, finish in 5 s")
                    }
                }

                // ── Grip-gated pose sending (v2 spec: each arm gated by its Grip) ──
                // DEBUG: Force sending even if grip is not pressed to verify connection
                xrWsClient?.sendState(state)

            } catch (e: Exception) {
                Log.e(TAG, "Error in stateSender", e)
            }
            stateSenderHandler.postDelayed(this, XR_STATE_SEND_INTERVAL_MS)
        }
    }

    private val videoServerUrl: String
        get() = intent?.getStringExtra("video_server_url") ?: "http://192.168.1.100:8000"
    private val videoStreamType: String
        get() = intent?.getStringExtra("stream_type") ?: "color"
    private val xrWsUrl: String
        get() = intent?.getStringExtra("xr_ws_url") ?: XrWsClient.RIGHT_ARM_URL

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility =
                (android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)

            if (!NativeBridge.isLibraryLoaded()) {
                Log.e(TAG, "Native library failed to load")
                finish(); return
            }
            if (!NativeBridge.nativeInit(this)) {
                Log.e(TAG, "Native init failed")
                finish(); return
            }
            nativeInitialized = true
            videoManager = VideoTextureManager(this)
            xrWsClient = XrWsClient(xrWsUrl)
            Log.i(TAG, "XRActivity initialized, ws=$xrWsUrl")
        } catch (e: Exception) {
            Log.e(TAG, "onCreate error", e)
            finish()
        }
    }

    override fun onResume() {
        super.onResume()
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnResume()
                videoManager?.startStream(videoServerUrl, videoStreamType)
                xrWsClient?.connect()
                stateSenderHandler.removeCallbacks(stateSender)
                stateSenderHandler.post(stateSender)
            }
        } catch (e: Exception) {
            Log.e(TAG, "onResume error", e)
        }
    }

    override fun onPause() {
        try {
            stateSenderHandler.removeCallbacks(stateSender)
            calibHandler.removeCallbacks(calibFinishRunnable)
            xrWsClient?.pause()
            if (nativeInitialized) {
                videoManager?.stopStream()
                NativeBridge.nativeOnPause()
            }
        } catch (e: Exception) {
            Log.e(TAG, "onPause error", e)
        }
        super.onPause()
    }

    override fun onDestroy() {
        try {
            stateSenderHandler.removeCallbacks(stateSender)
            calibHandler.removeCallbacks(calibFinishRunnable)
            xrWsClient?.disconnect()
            videoManager?.cleanup()
            if (nativeInitialized) NativeBridge.nativeRequestExit()
        } catch (e: Exception) {
            Log.e(TAG, "onDestroy error", e)
        }
        super.onDestroy()
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private fun sendCommand(cmdType: TeleopCommandType) {
        val cmd = TeleopCommand(
            tsMs = System.currentTimeMillis(),
            seq = ++cmdSeq,
            command = cmdType.value,
            note = cmdType.name,
        )
        xrWsClient?.sendCommand(cmd)
    }

    companion object {
        private const val TAG = "XRActivity"
        private const val XR_STATE_SEND_INTERVAL_MS = 20L  // 50 Hz
    }
}
