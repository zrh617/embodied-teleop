# VR视频流集成 - 快速检查清单

## ✅ 预装检查

- [ ] Python 3.8+ 已安装
- [ ] RealSense SDK已安装
- [ ] Android SDK已安装
- [ ] Quest 3设备已连接
- [ ] Quest 3已连接到WiFi

## 📦 文件检查

已创建以下文件：

### Python服务器文件
- [x] `d:\XRTeleoperation2\video_server.py` - 主服务器应用
- [x] `d:\XRTeleoperation2\start_video_server.bat` - Windows启动脚本
- [x] `d:\XRTeleoperation2\start_video_server.sh` - Linux/Mac启动脚本

### Java/Kotlin客户端文件
- [x] `app/src/main/java/com/xr/teleop/video/VideoStreamClient.kt` - 网络客户端
- [x] `app/src/main/java/com/xr/teleop/video/VideoTextureManager.kt` - 纹理管理器
- [x] `app/src/main/java/com/xr/teleop/XRActivityWithVideo.kt` - 增强Activity

### Native C++文件
- [x] `native/src/video/video_texture_jni.cpp` - JNI桥接代码

### 文档文件
- [x] `VIDEO_STREAM_INTEGRATION.md` - 完整集成指南
- [x] `USAGE_EXAMPLES.md` - 使用示例
- [x] `VIDEO_INTEGRATION_CHECKLIST.md` - 本文件

## 🚀 快速启动流程

### 第1步：启动视频服务器（5分钟）

**Windows:**
```bash
cd d:\XRTeleoperation2
start_video_server.bat
```

**预期输出:**
```
[重要] 在VR应用中使用以下URL:
  http://192.168.1.XXX:8000/stream/color
```

**记下你的IP地址：`192.168.1.XXX`**

### 第2步：修改应用清单（2分钟）

编辑 `app/src/main/AndroidManifest.xml`：

```xml
<!-- 停用旧Activity -->
<!-- <activity android:name=".XRActivity" ... /> -->

<!-- 启用新Activity -->
<activity android:name=".XRActivityWithVideo" android:screenOrientation="landscape">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

### 第3步：编译应用（3分钟）

```bash
cd d:\XRTeleoperation2
./gradlew.bat clean assembleDebug
```

**检查清单:**
- [ ] 编译成功（`BUILD SUCCESSFUL`）
- [ ] 没有错误（仅有警告是可以的）

### 第4步：安装到Quest 3（2分钟）

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

**检查清单:**
- [ ] 安装成功（`Success`）

### 第5步：启动应用（2分钟）

```bash
# 将 192.168.1.XXX 替换为你的PC IP
adb shell am start -n com.xr.teleop/.XRActivityWithVideo \
  -e video_server_url "http://192.168.1.XXX:8000" \
  -e stream_type "color"
```

### 第6步：验证连接（1分钟）

```bash
# 查看实时日志
adb logcat | grep -E "VideoStreamClient|VideoTextureManager"
```

**期望看到:**
```
I/VideoStreamClient: 开始连接到流服务器
I/VideoTextureManager: 帧已更新: 1280x720
```

**总耗时：约15分钟**

---

## 🔧 配置修改

### 改变视频源

```bash
# 使用深度图
adb shell am start -n com.xr.teleop/.XRActivityWithVideo \
  -e video_server_url "http://192.168.1.100:8000" \
  -e stream_type "depth"

# 或在应用中动态切换
videoTextureManager?.switchStreamType("depth")
```

### 优化性能

**降低分辨率（更低延迟）：**

编辑 `video_server.py` 第30行：
```python
# 改为640x480
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
```

**降低JPEG质量（更小带宽）：**

编辑 `video_server.py` 第100行：
```python
ok, jpg = cv2.imencode(".jpg", frame, [
    int(cv2.IMWRITE_JPEG_QUALITY), 60  # 改为60（范围0-100）
])
```

### 增加帧率（需要5GHz WiFi）

编辑 `video_server.py` 第30行：
```python
# 改为60 FPS
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 60)
```

---

## 🐛 故障排查

### 问题：无法连接到服务器

**症状：**
```
E/VideoStreamClient: 流接收错误: Connection refused
```

**解决步骤：**

```bash
# 1. 检查服务器是否运行
netstat -an | findstr :8000

# 2. 检查防火墙
netsh advfirewall firewall show rule name="Python FastAPI"

# 3. 验证网络连接
ping 192.168.1.100  # 从Quest设备

# 4. 检查IP地址（必须在同一子网）
ipconfig  # 获取你的网络配置
```

### 问题：视频卡顿或延迟大

**症状：**
- 看不到实时内容
- 帧率低于5 FPS

**解决步骤：**

```python
# video_server.py中：
# 1. 降低分辨率
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 2. 降低质量
cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])

# 3. 检查WiFi信号（需要-60dBm以上）
```

### 问题：应用启动时崩溃

**症状：**
```
E/libteleop: Exception in nativeUpdateVideoFrame
```

**解决步骤：**

```bash
# 1. 检查完整日志
adb logcat -v time | grep -A5 "nativeUpdateVideoFrame"

# 2. 确保所有文件都已创建
# 检查以下文件是否存在：
# - video_texture_jni.cpp
# - VideoStreamClient.kt
# - VideoTextureManager.kt
# - XRActivityWithVideo.kt

# 3. 检查CMakeLists.txt是否包含新源文件
grep "video_texture_jni.cpp" native/CMakeLists.txt
```

### 问题：内存不足

**症状：**
```
E/libteleop: Failed to allocate video buffer
```

**解决步骤：**

```kotlin
// 确保在onDestroy中调用cleanup
override fun onDestroy() {
    videoTextureManager?.cleanup()  // 释放所有资源
    super.onDestroy()
}

// 或减少缓冲区大小
// video_server.py中：
self.frame_buffer = deque(maxlen=1)  # 仅保留最新帧
```

---

## 📊 验证成功指标

| 指标 | 预期值 | 检查方法 |
|------|--------|---------|
| 服务器启动 | < 5秒 | 启动脚本输出 |
| 首次连接 | < 2秒 | logcat中出现"开始连接" |
| 首帧接收 | < 3秒 | logcat中出现"帧已更新" |
| 帧率 | 25-30 FPS | logcat中的帧更新频率 |
| 延迟 | < 500ms | 视觉观察 |
| 内存占用 | < 300 MB | `adb shell dumpsys meminfo` |

---

## 📱 应用启动参数参考

### 基本启动
```bash
adb shell am start -n com.xr.teleop/.XRActivityWithVideo
```

### 指定服务器和流类型
```bash
adb shell am start -n com.xr.teleop/.XRActivityWithVideo \
  -e video_server_url "http://192.168.1.100:8000" \
  -e stream_type "color"
```

### 其他可用参数
```bash
-e video_server_url "http://..."      # 视频服务器地址
-e stream_type "color"                 # 流类型: color或depth
-e log_level "verbose"                 # 日志级别
```

---

## 🔍 日志命令参考

```bash
# 查看所有视频相关日志
adb logcat | grep -i video

# 查看实时错误
adb logcat *:E | grep -i "video\|native"

# 导出日志到文件
adb logcat > video_debug.log

# 实时查看特定标签
adb logcat VideoStreamClient:V VideoTextureManager:V *:S

# 清空日志缓冲区
adb logcat -c
```

---

## 📚 文件结构回顾

```
d:\XRTeleoperation2/
├── video_server.py                          # Python FastAPI服务器
├── start_video_server.bat                   # Windows启动脚本
├── start_video_server.sh                    # Linux/Mac启动脚本
├── VIDEO_STREAM_INTEGRATION.md              # 详细集成指南
├── USAGE_EXAMPLES.md                        # 使用示例
├── app/
│   └── src/main/
│       ├── java/com/xr/teleop/
│       │   └── video/
│       │       ├── VideoStreamClient.kt     # 网络客户端
│       │       └── VideoTextureManager.kt   # 纹理管理
│       └── AndroidManifest.xml              # 需要修改以启用新Activity
├── native/
│   ├── CMakeLists.txt                       # 需要添加新源文件
│   └── src/video/
│       └── video_texture_jni.cpp            # JNI实现
└── gradle.properties, settings.gradle.kts等
```

---

## 💡 下一步

1. **基础集成完成后：**
   - [ ] 调整视频质量以匹配你的网络
   - [ ] 在VR场景中显示多个视频源
   - [ ] 添加UI控制以切换流类型

2. **进阶功能：**
   - [ ] 实现WebSocket低延迟传输
   - [ ] 添加本地录制功能
   - [ ] 支持点云可视化
   - [ ] 集成控制器交互

3. **优化和部署：**
   - [ ] 构建Release版本
   - [ ] 性能基准测试
   - [ ] 生产环境部署

---

## 📞 获取帮助

如果遇到问题：

1. **检查日志：** `adb logcat | grep -E "Video|Native|Error"`
2. **查看文档：** 参考 `VIDEO_STREAM_INTEGRATION.md`
3. **参考示例：** 查看 `USAGE_EXAMPLES.md`
4. **验证网络：** 使用ping和netstat检查连接

---

**祝您集成顺利！🎉**
