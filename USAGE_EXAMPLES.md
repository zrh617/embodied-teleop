# 完整使用示例

## 场景1: 快速开始（推荐用于首次设置）

### 第一次使用

#### 步骤1: 启动视频服务器

**Windows:**
```batch
cd d:\XRTeleoperation2
start_video_server.bat
```

**Linux/Mac:**
```bash
cd ~/XRTeleoperation2
chmod +x start_video_server.sh
./start_video_server.sh
```

预期输出：
```
========================================
  VR视频流服务快速启动
========================================

[1/4] 检查Python版本...
Python 3.11.x

[2/4] 虚拟环境已存在

[3/4] 激活虚拟环境并安装依赖...
...

[重要] 在VR应用中使用以下URL:
  http://192.168.1.100:8000/stream/color
  http://192.168.1.100:8000/stream/depth

========================================
  启动视频服务器
========================================

[2026-03-19 10:30:45] INFO:     Uvicorn running on http://0.0.0.0:8000
[2026-03-19 10:30:45] INFO:     Application startup complete
[2026-03-19 10:30:45] INFO:     RealSense初始化成功
[2026-03-19 10:30:45] INFO:     视频采集线程已启动
```

#### 步骤2: 修改应用配置

编辑 `app/src/main/AndroidManifest.xml`，确保使用新Activity：

```xml
<!-- 注释掉旧Activity -->
<!-- <activity android:name=".XRActivity" ... /> -->

<!-- 启用新Activity -->
<activity
    android:name=".XRActivityWithVideo"
    android:screenOrientation="landscape"
    android:immersive="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

#### 步骤3: 编译应用

```bash
cd d:\XRTeleoperation2

# 清理旧构建
./gradlew.bat clean

# 编译新版本（包含视频支持）
./gradlew.bat assembleDebug
```

编译过程中会自动编译新的 `video_texture_jni.cpp`。

#### 步骤4: 安装到Quest 3

```bash
# 安装APK
adb install -r app/build/outputs/apk/debug/app-debug.apk

# 输出应该显示
# Performing Streamed Install
# Success
```

#### 步骤5: 配置网络和启动应用

假设：
- PC IP: `192.168.1.100`
- Quest 3已连接到同一WiFi

启动应用并指定视频服务器：
```bash
adb shell am start -n com.xr.teleop/.XRActivityWithVideo \
  -e video_server_url "http://192.168.1.100:8000" \
  -e stream_type "color"
```

#### 步骤6: 验证连接

在实时日志中查看：
```bash
adb logcat | grep -E "VideoStreamClient|VideoTextureManager|VideoNativeBridge"
```

期望看到：
```
I/VideoStreamClient: 开始连接到流服务器: http://192.168.1.100:8000/stream/color
I/VideoStreamClient: 收到JPEG帧: 12345字节
I/VideoTextureManager: 帧已更新: 1280x720
I/VideoNativeBridge: Video frame updated: 1280x720 (3686400 bytes)
```

在VR设备上应该能看到来自RealSense摄像头的实时视频！

---

## 场景2: 从现有XRActivity中添加视频支持

如果不想替换整个Activity，可以在现有 `XRActivity.kt` 中添加视频功能。

### 步骤1: 修改XRActivity.kt

```kotlin
package com.xr.teleop

import android.app.Activity
import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import android.view.WindowManager
import com.xr.teleop.video.VideoTextureManager
import kotlinx.coroutines.*

class XRActivity : Activity() {
    private var nativeInitialized = false
    
    // ===== 添加视频支持 =====
    private var videoTextureManager: VideoTextureManager? = null
    private val activityScope = CoroutineScope(Dispatchers.Main + Job())
    
    companion object {
        private const val TAG = "XRActivity"
        // ===== 添加这些常量 =====
        private const val DEFAULT_VIDEO_SERVER = "http://192.168.1.100:8000"
        private const val DEFAULT_STREAM_TYPE = "color"
    }

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

            if (!NativeBridge.nativeInit(this)) {
                Log.e(TAG, "Native initialization failed")
                finish()
                return
            }
            nativeInitialized = true
            
            // ===== 添加视频初始化 =====
            initializeVideoManager()
            
            Log.i(TAG, "XRActivity initialized successfully")
        } catch (e: Exception) {
            Log.e(TAG, "Error during XRActivity.onCreate: ${e.message}", e)
            finish()
        }
    }

    // ===== 添加这个新函数 =====
    private fun initializeVideoManager() {
        videoTextureManager = VideoTextureManager(this)
        videoTextureManager?.setFrameUpdateCallback(object : VideoTextureManager.FrameUpdateCallback {
            override fun onFrameUpdated(bitmap: Bitmap) {
                val pixels = IntArray(bitmap.width * bitmap.height)
                bitmap.getPixels(pixels, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
                NativeBridge.nativeUpdateVideoFrame(pixels, bitmap.width, bitmap.height)
            }
            
            override fun onStreamError(error: String) {
                Log.e(TAG, "视频流错误: $error")
                NativeBridge.nativeSetStatus("video=error:$error")
            }
        })
    }

    override fun onResume() {
        super.onResume()
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnResume()
                
                // ===== 添加视频流启动 =====
                val serverUrl = intent?.getStringExtra("video_server_url") ?: DEFAULT_VIDEO_SERVER
                val streamType = intent?.getStringExtra("stream_type") ?: DEFAULT_STREAM_TYPE
                videoTextureManager?.startStream(serverUrl, streamType)
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error during onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
            if (nativeInitialized) {
                NativeBridge.nativeOnPause()
                // ===== 添加视频流停止 =====
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
            // ===== 添加清理 =====
            videoTextureManager?.cleanup()
            activityScope.cancel()
        } catch (e: Exception) {
            Log.e(TAG, "Error during onDestroy: ${e.message}", e)
        }
        super.onDestroy()
    }
}
```

### 步骤2: 修改NativeBridge.kt

在 `NativeBridge.kt` 中添加视频相关的native方法声明：

```kotlin
object NativeBridge {
    // ... 现有方法 ...

    // ===== 添加这些方法 =====
    external fun nativeUpdateVideoFrame(pixelData: IntArray, width: Int, height: Int)
    external fun nativeSetStatus(status: String)

    companion object {
        init {
            System.loadLibrary("teleop")
        }
    }
}
```

### 步骤3: 修改CMakeLists.txt

在 `native/CMakeLists.txt` 中添加新的JNI源文件：

```cmake
add_library(${CMAKE_PROJECT_NAME} SHARED
    src/app/jni_entry.cpp
    src/app/app_main.cpp
    src/xr/xr_instance.cpp
    src/xr/xr_session.cpp
    src/xr/xr_frame_loop.cpp
    src/xr/xr_actions.cpp
    src/renderer/vk_context.cpp
    src/renderer/mesh_curved_screen.cpp
    src/renderer/video_pipeline.cpp
    src/renderer/hud_renderer.cpp
    src/video/video_texture_bridge.cpp
    src/video/video_timing.cpp
    src/video/video_texture_jni.cpp  # 添加这一行
    src/input/pose_provider.cpp
    src/input/controller_input.cpp
    src/common/log.cpp
    src/common/time.cpp
)
```

### 步骤4: 编译和测试

```bash
cd d:\XRTeleoperation2
./gradlew.bat clean assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

---

## 场景3: 使用WebSocket实现低延迟流式传输

对于需要更低延迟的应用，可以使用WebSocket替代HTTP。

### 修改Python服务器

```python
# 在video_server.py中添加WebSocket支持
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/video/color")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame = video_server.get_latest_frame('color')
            if frame is not None:
                _, jpg = cv2.imencode(".jpg", frame, 
                    [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                # 发送二进制帧
                await websocket.send_bytes(jpg.tobytes())
            await asyncio.sleep(1.0 / 30)  # 30 FPS
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
```

### 修改Kotlin客户端

```kotlin
// 使用OkHttp的WebSocket
import okhttp3.WebSocket
import okhttp3.WebSocketListener

class WebSocketVideoClient {
    private val httpClient = OkHttpClient()
    
    fun connectWebSocket(url: String) {
        val request = Request.Builder()
            .url(url)
            .build()
        
        val listener = object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                val bitmap = BitmapFactory.decodeByteArray(
                    bytes.toByteArray(), 0, bytes.size()
                )
                // 更新帧
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e(TAG, "WebSocket error: ${t.message}")
            }
        }
        
        httpClient.newWebSocket(request, listener)
    }
}
```

---

## 场景4: 添加双视图（彩色+深度同时显示）

```kotlin
// 在VideoTextureManager中支持多个流
class DualVideoTextureManager(context: Context) {
    private val colorManager = VideoTextureManager(context)
    private val depthManager = VideoTextureManager(context)
    
    fun startDualStreams(baseUrl: String) {
        colorManager.startStream(baseUrl, "color")
        depthManager.startStream(baseUrl, "depth")
    }
    
    fun stopDualStreams() {
        colorManager.stopStream()
        depthManager.stopStream()
    }
}
```

在Native端分别处理两个纹理，并在VR场景中并排显示。

---

## 场景5: 本地测试（无RealSense摄像头）

### 使用测试图像替代

```python
# 修改video_server.py
def test_mode_gen_frames():
    """生成测试图像而不是从RealSense读取"""
    import numpy as np
    
    while True:
        # 创建彩色梯度图像
        img = np.zeros((720, 1280, 3), dtype=np.uint8)
        for i in range(1280):
            img[:, i] = [i % 256, (i // 2) % 256, (i // 3) % 256]
        
        yield img
```

### 模拟HTTP端点

```python
@app.get("/stream/color")
async def stream_color():
    # 使用测试帧而非RealSense
    async def test_stream_gen():
        for frame in test_mode_gen_frames():
            ok, jpg = cv2.imencode(".jpg", frame)
            yield b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"
    
    return StreamingResponse(test_stream_gen(), media_type="multipart/x-mixed-replace; boundary=frame")
```

---

## 常见问题排查

### Q: 看不到视频，只看到黑色或错误信息

**A:** 检查以下几点：

```bash
# 1. 服务器是否运行
netstat -an | findstr 8000

# 2. 连接性
ping 192.168.1.100

# 3. 应用日志
adb logcat | grep "VideoStreamClient"

# 4. RealSense摄像头
# 在PC上运行
python -c "import pyrealsense2; print('OK')"
```

### Q: 帧率很低，视频卡顿

**A:** 

```python
# video_server.py中降低分辨率和质量
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])  # 降低质量
```

### Q: 应用崩溃或内存溢出

**A:**

```kotlin
// 确保在onDestroy中清理
override fun onDestroy() {
    videoTextureManager?.cleanup()  // 必须调用
    super.onDestroy()
}
```

---

## 性能指标

| 配置 | 分辨率 | 帧率 | 带宽 | 延迟 | 备注 |
|------|--------|------|------|------|------|
| 高质量 | 1280x720 | 30 | ~10 Mbps | 500ms | 需要5GHz WiFi |
| 平衡 | 960x540 | 30 | ~5 Mbps | 300ms | 推荐配置 |
| 低延迟 | 640x480 | 30 | ~2 Mbps | 100ms | 用于对延迟敏感的应用 |
| WebSocket | 640x360 | 30 | ~1 Mbps | <50ms | 最低延迟选项 |

