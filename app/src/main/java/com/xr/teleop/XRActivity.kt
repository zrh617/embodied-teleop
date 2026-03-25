package com.xr.teleop

import android.app.Activity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.WindowManager
import com.xr.teleop.video.VideoTextureManager
import com.xr.teleop.xr.XrWsClient
import com.xr.teleop.xr.createTestXrControllerState

class XRActivity : Activity() {
    private var nativeInitialized = false
    private var videoManager: VideoTextureManager? = null
    private var xrWsClient: XrWsClient? = null
    private val stateSenderHandler = Handler(Looper.getMainLooper())
    private val stateSender = object : Runnable {
        override fun run() {
            xrWsClient?.sendState(createTestXrControllerState())
            stateSenderHandler.postDelayed(this, XR_STATE_SEND_INTERVAL_MS)
        }
    }

    // Change this to your server's IP and port
    private val videoServerUrl: String
        get() = intent?.getStringExtra("video_server_url") ?: "http://192.168.1.100:8000"
    private val videoStreamType: String
        get() = intent?.getStringExtra("stream_type") ?: "color"
    private val xrWsUrl: String
        get() = intent?.getStringExtra("xr_ws_url") ?: XrWsClient.DEFAULT_URL

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        try {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            window.decorView.systemUiVisibility =
                (android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)

            if (!NativeBridge.isLibraryLoaded()) {
                Log.e(TAG, "Native library failed to load, cannot initialize XR")
                finish()
                return
            }

            if (!NativeBridge.nativeInit(this)) {
                Log.e(TAG, "Native initialization failed")
                finish()
                return
            }
            nativeInitialized = true
            videoManager = VideoTextureManager(this)
            xrWsClient = XrWsClient(xrWsUrl)
            Log.i(TAG, "XRActivity initialized successfully")
        } catch (e: Exception) {
            Log.e(TAG, "Error during XRActivity.onCreate: ${e.message}", e)
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
                Log.i(TAG, "Video stream started: $videoServerUrl/$videoStreamType")
                Log.i(TAG, "XR state reporting started: $xrWsUrl")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
            stateSenderHandler.removeCallbacks(stateSender)
            xrWsClient?.disconnect()
            if (nativeInitialized) {
                videoManager?.stopStream()
                NativeBridge.nativeOnPause()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onPause: ${e.message}", e)
        }
        super.onPause()
    }

    override fun onDestroy() {
        try {
            stateSenderHandler.removeCallbacks(stateSender)
            xrWsClient?.disconnect()
            videoManager?.cleanup()
            if (nativeInitialized) {
                NativeBridge.nativeRequestExit()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onDestroy: ${e.message}", e)
        }
        super.onDestroy()
    }

    companion object {
        private const val TAG = "XRActivity"
        private const val XR_STATE_SEND_INTERVAL_MS = 50L
    }
}
