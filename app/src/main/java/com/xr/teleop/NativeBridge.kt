package com.xr.teleop

import android.app.Activity
import android.util.Log

object NativeBridge {
    private const val TAG = "NativeBridge"
    private var libraryLoaded = false

    init {
        try {
            System.loadLibrary("teleop")
            libraryLoaded = true
            Log.i(TAG, "Native library 'teleop' loaded successfully")
        } catch (e: UnsatisfiedLinkError) {
            Log.e(TAG, "Failed to load native library 'teleop': ${e.message}", e)
            libraryLoaded = false
        } catch (e: Exception) {
            Log.e(TAG, "Unexpected error loading native library: ${e.message}", e)
            libraryLoaded = false
        }
    }

    external fun nativeInit(activity: Activity): Boolean
    external fun nativeOnResume()
    external fun nativeOnPause()
    external fun nativeRequestExit()
    external fun nativeGetStatus(): String
    external fun nativeGetControllerStateJson(): String

    // Push a decoded video frame (Android ARGB_8888 int array) into the native renderer.
    external fun nativeUpdateVideoFrame(pixelData: IntArray, width: Int, height: Int)

    fun isLibraryLoaded(): Boolean = libraryLoaded
}
