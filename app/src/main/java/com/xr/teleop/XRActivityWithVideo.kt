package com.xr.teleop

import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import android.view.WindowManager
import android.app.Activity
import com.xr.teleop.video.VideoTextureManager
import kotlinx.coroutines.*

/**
 * 增强的XR活动，集成视频流显示
 * 支持直接显示RealSense视频到VR场景中
 */
class XRActivityWithVideo : Activity() {
    companion object {
        private const val TAG = "XRActivityWithVideo"
        
        // 配置参数
        private const val DEFAULT_SERVER_URL = "http://192.168.1.100:8000"
        private const val STREAM_TYPE_COLOR = "color"
        private const val STREAM_TYPE_DEPTH = "depth"
    }

    private var nativeInitialized = false
    private var videoTextureManager: VideoTextureManager? = null
    private val activityScope = CoroutineScope(Dispatchers.Main + Job())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        try {
            // 设置全屏模式
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility =
                (android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_FULLSCREEN
                    or android.view.View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or android.view.View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)

            // 初始化Native代码
            if (!NativeBridge.nativeInit(this)) {
                Log.e(TAG, "Native initialization failed")
                finish()
                return
            }
            nativeInitialized = true
            
            // 初始化视频管理器
            initializeVideoManager()
            
            Log.i(TAG, "XRActivity with video initialized successfully")
        } catch (e: Exception) {
            Log.e(TAG, "Error during XRActivity.onCreate: ${e.message}", e)
            finish()
        }
    }

    /**
     * 初始化视频管理器并设置回调
     */
    private fun initializeVideoManager() {
        videoTextureManager = VideoTextureManager(this)
        
        videoTextureManager?.setFrameUpdateCallback(object : VideoTextureManager.FrameUpdateCallback {
            override fun onFrameUpdated(bitmap: Bitmap) {
                // 当新帧到达时，将其传递给Native渲染器
                onVideoFrameReceived(bitmap)
            }

            override fun onStreamError(error: String) {
                Log.e(TAG, "视频流错误: $error")
                NativeBridge.nativeSetStatus("video=error:$error")
            }
        })
    }

    /**
     * 启动视频流接收
     * 可以从配置文件或Intent获取服务器地址
     */
    private fun startVideoStream() {
        try {
            val serverUrl = getServerUrl()
            val streamType = getStreamType()
            
            Log.i(TAG, "启动视频流: $serverUrl/$streamType")
            NativeBridge.nativeSetStatus("video=connecting")
            
            videoTextureManager?.startStream(serverUrl, streamType)
        } catch (e: Exception) {
            Log.e(TAG, "启动视频流失败", e)
            NativeBridge.nativeSetStatus("video=error:${e.message}")
        }
    }

    /**
     * 处理接收到的视频帧
     * 将Bitmap转换为Native可用的格式
     */
    private fun onVideoFrameReceived(bitmap: Bitmap) {
        try {
            // 提取Bitmap像素数据
            val width = bitmap.width
            val height = bitmap.height
            val pixelArray = IntArray(width * height)
            bitmap.getPixels(pixelArray, 0, width, 0, 0, width, height)
            
            // 将帧数据传递给Native渲染器
            NativeBridge.nativeUpdateVideoFrame(pixelArray, width, height)
            
            Log.d(TAG, "视频帧已更新: ${width}x${height}")
        } catch (e: Exception) {
            Log.e(TAG, "处理视频帧失败", e)
        }
    }

    /**
     * 从Intent获取服务器地址
     */
    private fun getServerUrl(): String {
        return intent?.getStringExtra("video_server_url") ?: DEFAULT_SERVER_URL
    }

    /**
     * 从Intent获取流类型
     */
    private fun getStreamType(): String {
        return intent?.getStringExtra("stream_type") ?: STREAM_TYPE_COLOR
    }

    override fun onResume() {
        super.onResume()
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnResume()
                // 恢复时重新启动视频流
                startVideoStream()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnPause()
                // 暂停时停止视频流
                videoTextureManager?.stopStream()
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
            // 清理视频资源
            videoTextureManager?.cleanup()
            activityScope.cancel()
        } catch (e: Exception) {
            Log.e(TAG, "Error during onDestroy: ${e.message}", e)
        }
        super.onDestroy()
    }

    /**
     * 切换流类型（彩色/深度）
     */
    fun switchStreamType(streamType: String) {
        videoTextureManager?.stopStream()
        activityScope.launch {
            delay(500)
            videoTextureManager?.startStream(getServerUrl(), streamType)
        }
    }
}

/**
 * NativeBridge扩展，支持视频帧更新
 * 这些函数应该在native代码中实现
 */
object NativeBridgeVideoExtension {
    init {
        // native库应该已经被加载
    }

    /**
     * 更新视频帧到GPU纹理
     */
    external fun nativeUpdateVideoFrame(pixelData: IntArray, width: Int, height: Int)

    /**
     * 设置应用状态文本
     */
    external fun nativeSetStatus(status: String)
}
