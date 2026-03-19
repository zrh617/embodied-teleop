package com.xr.teleop

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.WindowManager
import com.xr.teleop.video.VideoTextureManager

class XRActivity : Activity() {
    private var nativeInitialized = false
    private var videoManager: VideoTextureManager? = null

    // Change this to your server's IP and port
    private val videoServerUrl: String
        get() = intent?.getStringExtra("video_server_url") ?: "http://192.168.1.100:8000"
    private val videoStreamType: String
        get() = intent?.getStringExtra("stream_type") ?: "color"

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
                Log.i(TAG, "Video stream started: $videoServerUrl/$videoStreamType")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
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
    }
}
