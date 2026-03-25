# XRTeleoperation

面向 Meta Quest 的原生 Android XR 遥操作客户端。当前工程包含两条核心链路：

- Quest 端进入 `XRActivity` 后加载原生 XR 能力，并拉取远端视频流
- Quest 端通过 WebSocket 主动向 Ubuntu/ROS 侧持续上报头显和手柄状态

当前 WebSocket 上报已经固定为 `xr_controller_state` JSON 文本帧，Ubuntu 侧可直接使用仓库根目录的 `xr_ws_bridge.py` 做接收和二次转发。

## 功能概览

- 原生 Android Activity 作为 Quest 沉浸式入口
- OpenXR / Native 层初始化入口已接入 `NativeBridge`
- 视频流播放入口已接入 `VideoTextureManager`
- OkHttp WebSocket 客户端持续上报 XR 状态
- 提供 Python WebSocket 桥接脚本，便于接 ROS 或日志验证
- 当前发送的是固定测试数据，便于先打通 Quest -> Ubuntu -> ROS 链路

## 工程结构

- `app/src/main/java/com/xr/teleop/XRActivity.kt`
  Quest 主入口，负责原生初始化、视频流启动、WebSocket 连接和定时发送状态
- `app/src/main/java/com/xr/teleop/xr/XrWsClient.kt`
  OkHttp WebSocket 客户端封装
- `app/src/main/java/com/xr/teleop/xr/XrControllerState.kt`
  XR 状态数据结构、JSON 序列化和测试数据生成
- `xr_ws_bridge.py`
  Ubuntu 侧 WebSocket 接收示例，当前会解析消息并打印，可继续接 ROS publisher
- `native/`
  原生 XR / 渲染相关代码和 CMake 配置

## 运行架构

```text
Video Server  ----HTTP---->  Quest App (XRActivity)
                                   |
                                   | WebSocket JSON
                                   v
                         ws://<Ubuntu_IP>:8765
                                   |
                                   v
                             xr_ws_bridge.py
                                   |
                                   v
                                  ROS
```

## 环境要求

- Android Studio
- Android SDK 36
- Android NDK
- CMake 3.22.1
- Meta Quest 设备
- Ubuntu 主机与 Quest 处于同一网段

## 默认配置

### Quest 端默认地址

- 视频流地址：`http://192.168.1.100:8000`
- 视频流类型：`color`
- XR WebSocket 地址：`ws://192.168.147.131:8765`

这些值当前在 `XRActivity` 中通过 `Intent` extra 支持覆盖：

- `video_server_url`
- `stream_type`
- `xr_ws_url`

### WebSocket 地址注意事项

Quest 端必须连接 Ubuntu 真实可访问 IP，例如：

```text
ws://192.168.147.131:8765
```

不要使用：

- `ws://0.0.0.0:8765`
- `ws://localhost:8765`

建议：

- Quest 与 Ubuntu 在同一网段
- 虚拟机网络使用桥接模式
- Ubuntu 上已启动 `xr_ws_bridge.py`

## XR 状态消息格式

Quest 端当前持续发送如下结构：

```json
{
  "type": "xr_controller_state",
  "ts_ms": 1710000000000,
  "seq": 123,
  "head": {
    "pos": { "x": 0.0, "y": 1.5, "z": 0.2 },
    "rot": { "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 }
  },
  "left": {
    "connected": true,
    "pos": { "x": -0.2, "y": 1.2, "z": 0.4 },
    "rot": { "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 },
    "thumbstick": { "x": 0.0, "y": 0.0 },
    "trigger": 0.0,
    "squeeze": 0.0,
    "buttons": {
      "primary": false,
      "secondary": false,
      "thumbstick_click": false,
      "menu": false,
      "system": false
    }
  },
  "right": {
    "connected": true,
    "pos": { "x": 0.2, "y": 1.2, "z": 0.4 },
    "rot": { "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 },
    "thumbstick": { "x": 0.0, "y": 0.0 },
    "trigger": 0.0,
    "squeeze": 0.0,
    "buttons": {
      "primary": false,
      "secondary": false,
      "thumbstick_click": false,
      "menu": false,
      "system": false
    }
  }
}
```

字段约定：

- `type`：消息类型，固定为 `xr_controller_state`
- `ts_ms`：毫秒时间戳
- `seq`：递增序号，用于排查丢包或乱序
- `head`：头显位姿
- `left` / `right`：左右手柄状态
- `rot`：统一使用四元数 `{x, y, z, w}`
- `thumbstick` / `trigger` / `squeeze` / `buttons`：控制输入拆分展开

## Quest 端当前行为

`XRActivity` 在生命周期中的行为如下：

- `onCreate`
  初始化原生 XR，创建视频管理器和 WebSocket 客户端
- `onResume`
  启动视频流，连接 WebSocket，并以 20Hz 持续发送测试状态
- `onPause` / `onDestroy`
  停止发送、关闭 WebSocket、清理视频资源

当前发送的是 `createTestXrControllerState()` 生成的固定测试数据，还没有接入真实 OpenXR 头显/手柄追踪值。

## Ubuntu 侧桥接脚本

仓库根目录提供了 `xr_ws_bridge.py`，默认监听：

```text
ws://0.0.0.0:8765
```

启动方式：

```bash
python3 xr_ws_bridge.py
```

依赖安装：

```bash
pip install websockets
```

当前脚本行为：

- 接收 Quest 发来的 JSON 文本帧
- 校验 `type == "xr_controller_state"`
- 解析 `ts_ms`、`seq`、`head`、`left`、`right`
- 打印关键状态日志
- 返回 `{"ok": true, "seq": ...}` 确认消息

后续如果接入 ROS，推荐直接在 `publish_state()` 中替换为 ROS publisher 逻辑。

## 构建与安装

### 1. 构建 APK

在项目根目录执行：

```powershell
.\gradlew.bat :app:assembleDebug
```

### 2. 安装到 Quest

```powershell
adb install -r .\app\build\outputs\apk\debug\app-debug.apk
```

### 3. 启动应用

安装完成后，可在 Quest 中直接启动应用。当前入口 Activity 为 `XRActivity`，已声明为沉浸式 HMD 入口。

## Manifest 与权限

工程当前声明了以下关键权限与特性：

- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`
- `com.oculus.permission.USE_SCENE`
- `android.hardware.vr.headtracking`
- `com.oculus.feature.PASSTHROUGH`

同时应用开启了：

- `android:usesCleartextTraffic="true"`

因此默认支持当前工程中的明文 `http://` 视频流地址和 `ws://` WebSocket 地址。

## 联调建议

建议按下面顺序打通链路：

1. 先在 Ubuntu 上启动 `xr_ws_bridge.py`
2. 确认 Quest 能访问 `ws://<Ubuntu_IP>:8765`
3. 启动 Quest 应用，观察 Ubuntu 日志中是否持续收到 `seq`
4. 确认 WebSocket 链路稳定后，再把固定测试数据替换成真实 OpenXR 数据
5. 最后在 `publish_state()` 中接入 ROS topic 发布

## 常见问题

### Quest 连不上 WebSocket

优先检查：

- 是否用了 Ubuntu 的真实 IP，而不是 `localhost`
- Quest 和 Ubuntu 是否在同一网段
- 虚拟机网络是否为桥接模式
- Ubuntu 防火墙是否放通 `8765`
- `xr_ws_bridge.py` 是否已经启动

### Ubuntu 能收到连接但没有有效数据

优先检查：

- Quest 发送的是不是文本 JSON 帧
- `type` 是否为 `xr_controller_state`
- 字段名是否仍然与当前 schema 一致

### 视频流无法播放

优先检查：

- `video_server_url` 是否可从 Quest 访问
- 服务端是否真的在对应端口提供视频流
- `stream_type` 是否与服务端路由一致

## 后续开发建议

- 将 `createTestXrControllerState()` 替换为真实 OpenXR pose / input 数据
- 在 Quest 端加入断线重连和连接状态提示
- 在 Ubuntu 侧桥接脚本中接 ROS topic / TF 发布
- 根据坐标系约定补充 Quest 与 ROS 侧的轴向映射和标定
