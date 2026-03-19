# VR应用视频流集成指南

## 概述

本指南说明如何将RealSense摄像头的视频流直接显示到Meta Quest 3 VR应用中。系统采用了C/S架构：

- **服务器端**：Python FastAPI服务器运行RealSense SDK，通过HTTP MJPEG流式传输视频
- **客户端**：VR应用接收流、解码帧并显示到VR场景中

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    PC (Windows/Linux)                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          RealSense摄像头                             │  │
│  │          (彩色 + 深度 传感器)                        │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │        FastAPI视频服务器 (video_server.py)           │  │
│  │  • 初始化RealSense pipeline                          │  │
│  │  • 后台采集彩色+深度帧                               │  │
│  │  • MJPEG编码和HTTP流式传输                          │  │
│  │  • /stream/color 和 /stream/depth 端点              │  │
│  └────────────────┬────────────────────────────────────┘  │
│                   │ HTTP (port 8000)                       │
└───────────────────┼────────────────────────────────────────┘
                    │
      WiFi/网络连接 │
                    │
┌───────────────────▼────────────────────────────────────────┐
│              Meta Quest 3 (VR设备)                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            XRActivity with Video                     │  │
│  │  • 初始化VideoTextureManager                        │  │
│  │  • 启动VideoStreamClient接收MJPEG流                 │  │
│  │  • 解码单个JPEG帧                                   │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │ Bitmap                                    │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │        Native Video Bridge (JNI)                    │  │
│  │  • Java→C++像素数据转换                            │  │
│  │  • ARGB → RGBA转换                                 │  │
│  │  • Vulkan纹理更新                                  │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │     Vulkan渲染器 (VR场景显示)                      │  │
│  │  • 创建GPU纹理                                     │  │
│  │  • 在四边形面板上显示视频                          │  │
│  │  • OpenXR合成                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 快速开始

### 第1步：启动Python视频服务器

#### 前置条件
```bash
# 安装依赖
pip install fastapi uvicorn opencv-python numpy pyrealsense2 okhttp3

# 确保RealSense SDK已安装
# Windows: 从 https://github.com/IntelRealSense/librealsense/releases 下载
# Linux: sudo apt install librealsense2-dev
```

#### 启动服务器
```bash
cd d:\XRTeleoperation2

# 直接运行
python video_server.py

# 或使用uvicorn
uvicorn video_server:app --host 0.0.0.0 --port 8000 --reload
```

### 第2步：修改VR应用配置

#### 方案A：使用新的XRActivityWithVideo（推荐）

编辑 `AndroidManifest.xml`：
```xml
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

#### 方案B：使用Intent参数启动

从命令行启动应用并指定视频服务器地址：
```bash
adb shell am start -n com.xr.teleop/.XRActivityWithVideo \
  -e video_server_url "http://192.168.1.100:8000" \
  -e stream_type "color"
```

### 第3步：编译和部署

```bash
cd d:\XRTeleoperation2

# 编译
./gradlew.bat clean assembleDebug

# 部署到Quest 3
adb install -r app/build/outputs/apk/debug/app-debug.apk

# 启动应用
adb shell am start -n com.xr.teleop/.XRActivityWithVideo
```

### 第4步：验证连接

在PC上查看服务器日志：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     RealSense初始化成功
INFO:     视频采集线程已启动
```

在VR应用中检查状态（通过adb logcat）：
```bash
adb logcat | grep "VideoTextureManager\|VideoStreamClient"

# 输出应该包含
# VideoStreamClient: 开始连接到流服务器
# VideoTextureManager: 帧已更新: 1280x720
```

## 详细说明

### Python服务器配置

#### 调整性能参数

在 `video_server.py` 中修改：

```python
# 增加帧率
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 60)  # 改为60 FPS

# 减少分辨率以降低延迟
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 调整JPEG质量
ok, jpg = cv2.imencode(".jpg", frame, [
    int(cv2.IMWRITE_JPEG_QUALITY), 85,  # 增加质量（0-100，越高越好）
])
```

#### 多客户端支持

当前实现为单客户端。支持多个VR客户端需要：

```python
# 使用消息队列或多线程广播
from threading import RLock

class RealSenseVideoServer:
    def __init__(self):
        self.clients = {}
        self.clients_lock = RLock()
    
    def add_client(self, client_id):
        with self.clients_lock:
            self.clients[client_id] = {'buffer': deque(maxlen=2)}
    
    def broadcast_frame(self, frame):
        with self.clients_lock:
            for client in self.clients.values():
                client['buffer'].append(frame)
```

### VR应用集成

#### 在现有Activity中集成

如果要在现有的 `XRActivity.kt` 中添加视频支持：

```kotlin
class XRActivity : Activity() {
    private var videoTextureManager: VideoTextureManager? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // ... 现有初始化代码 ...
        
        // 添加视频管理
        videoTextureManager = VideoTextureManager(this)
        videoTextureManager?.setFrameUpdateCallback(object : VideoTextureManager.FrameUpdateCallback {
            override fun onFrameUpdated(bitmap: Bitmap) {
                NativeBridge.nativeUpdateVideoFrame(bitmap.pixels, bitmap.width, bitmap.height)
            }
            override fun onStreamError(error: String) {
                Log.e(TAG, "视频错误: $error")
            }
        })
    }
    
    override fun onResume() {
        super.onResume()
        videoTextureManager?.startStream("http://YOUR_PC_IP:8000", "color")
    }
    
    override fun onPause() {
        videoTextureManager?.stopStream()
        super.onPause()
    }
    
    override fun onDestroy() {
        videoTextureManager?.cleanup()
        super.onDestroy()
    }
}
```

#### JNI绑定

确保在 `CMakeLists.txt` 中编译新的JNI源文件：

```cmake
add_library(${CMAKE_PROJECT_NAME} SHARED
    # ... 现有源文件 ...
    src/video/video_texture_jni.cpp  # 添加这行
)
```

### 网络配置

#### 设置PC和Quest 3在同一网络

1. **PC端**：
   - 查找PC的IP地址：`ipconfig` (Windows) 或 `ifconfig` (Linux)
   - 记下本地IP，例如 `192.168.1.100`

2. **Quest 3端**：
   - 连接到同一个WiFi网络
   - 在应用中使用PC的IP启动流：
     ```kotlin
     videoTextureManager?.startStream("http://192.168.1.100:8000", "color")
     ```

#### 防火墙配置

如果连接不成功，检查防火墙：

**Windows:**
```powershell
# 允许Python通过防火墙
netsh advfirewall firewall add rule name="Python FastAPI" dir=in action=allow program="C:\path\to\python.exe" enable=yes

# 或手动在Windows防火墙中添加端口 8000
```

**Linux:**
```bash
sudo ufw allow 8000
```

## 调试和常见问题

### 问题1：无法连接到服务器

**症状**：`VideoStreamClient: 流接收错误: Connection refused`

**解决方案**：
```bash
# 1. 检查服务器是否运行
netstat -an | findstr 8000  # Windows
lsof -i :8000              # Linux/Mac

# 2. 检查防火墙
ping <PC_IP>  # 从Quest设备

# 3. 检查网络连接
ipconfig  # 确保Quest和PC在同一子网
```

### 问题2：帧率过低或延迟高

**症状**：视频卡顿或延迟大于1秒

**解决方案**：
```python
# 在 video_server.py 中：
# 1. 降低分辨率
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 2. 降低JPEG质量
cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])

# 3. 检查网络带宽
# 估算: 1280x720 @ 30fps MJPEG ≈ 5-15 Mbps（取决于质量）
# 5GHz WiFi建议
```

### 问题3：应用崩溃

**查看日志**：
```bash
adb logcat | grep -E "VideoNativeBridge|VideoTextureManager|crash"

# 常见错误
# E/VideoNativeBridge: Invalid video frame parameters
#   → 检查宽高是否> 0
# 
# E/VideoNativeBridge: Failed to get pixel array
#   → JNI异常，检查Java端像素数据
```

### 问题4：内存泄漏

**症状**：长时间运行后应用变慢或崩溃

**解决方案**：
```kotlin
// 在VideoTextureManager中确保清理
override fun onDestroy() {
    videoTextureManager?.cleanup()  // 必须调用
    super.onDestroy()
}

// 在native代码中确保释放纹理
// 见video_texture_jni.cpp的析构函数
```

## 性能优化建议

| 参数 | 用途 | 默认值 | 优化建议 |
|------|------|--------|---------|
| 分辨率 | 视频清晰度 | 1280x720 | 高延迟时降至640x480 |
| 帧率 | 流畅度 | 30 FPS | WiFi 6时可提升至60 FPS |
| JPEG质量 | 压缩率 | 75% | 低带宽时降至60% |
| 缓冲区大小 | 内存vs延迟 | 2帧 | 增加到3-4降低抖动 |

## 扩展功能

### 1. 切换彩色/深度流

```kotlin
// 在Activity中
fun toggleStreamType() {
    val currentType = intent.getStringExtra("stream_type") ?: "color"
    val newType = if (currentType == "color") "depth" else "color"
    intent.putExtra("stream_type", newType)
    videoTextureManager?.switchStreamType(newType)
}
```

### 2. 添加点云显示

```python
# 在video_server.py中导出点云数据
@app.get("/pointcloud")
async def get_pointcloud():
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    
    # 使用pyrealsense2的点云处理
    pc = rs.pointcloud()
    points = pc.calculate(depth_frame)
    points_list = points.get_vertices()
    
    # 序列化为JSON
    return {"points": points_list}
```

### 3. 添加录制功能

```python
# 记录视频到本地文件
import av

def record_video():
    container = av.open('output.mp4', 'w')
    stream = container.add_stream('h264', rate=30)
    stream.height = 720
    stream.width = 1280
    
    while recording:
        frame = get_latest_frame()
        av_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
        for packet in stream.encode(av_frame):
            container.mux(packet)
```

## 参考资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [RealSense Python API](https://github.com/IntelRealSense/librealsense/blob/master/doc/Python_API.md)
- [OpenXR规范](https://www.khronos.org/openxr/)
- [Android JNI最佳实践](https://developer.android.com/training/articles/on-device-debugging)
- [Meta Quest开发文档](https://developer.oculus.com/documentation/)

## 支持

如遇到问题，请检查：
1. 应用日志: `adb logcat`
2. 服务器日志：查看Python console输出
3. 网络连接：ping和netstat命令
4. 系统要求：Python 3.8+, RealSense SDK, Android API 33+
