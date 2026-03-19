package com.xr.teleop

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.WindowManager

class XRActivity : Activity() {
    private var nativeInitialized = false

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

            if (!NativeBridge.nativeInit(this)) {
                Log.e(TAG, "Native initialization failed")
                finish()
                return
            }
            nativeInitialized = true
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
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnPause()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onPause: ${e.message}", e)
        }
        super.onPause()
    }

    override fun onDestroy() {
        try {
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
