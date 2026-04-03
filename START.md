# 完整启动与使用流程

## 一、环境准备

### 服务端（PC / 机器人控制电脑）

- 确保 Python 环境和依赖已安装。
- 确认机器人控制电脑 IP 为 `10.20.200.46`。
- 确认 CPS 控制器端口 `10003` 已开放。

---

## 二、启动服务端 `ws_to_servop.py`

### 默认参数

- 监听 `ws://0.0.0.0:8765`（等待 Quest 连入）
- 连接机器人 `10.20.200.46:10003`
- 控制右臂（`--side right`）

### 启动命令示例

```bash
python3 ws_to_servop.py \
  --cps-ip 10.20.200.46 \
  --side right \
  --x-offset-mm 420 \
  --y-offset-mm 445 \
  --z-offset-mm 180 \
  --rx-offset-deg 180 \
  --rz-offset-deg -90
```

### 启动后预期日志

- `[robot] connected to 10.20.200.46:10003`
- `[ws] listening on ws://0.0.0.0:8765`

---

## 三、构建并安装 Android APK

在 Cursor / Android Studio 中构建:
```bash
cd /Users/zhengruihang/Documents/embodied-teleop
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```
或直接在 Android Studio 点击 **Run**，通过 USB 安装到 Quest。

---

## 四、Quest 头显操作流程

### Step 1：启动 App

- 戴上 Quest，打开 XR Teleop 应用。
- App 自动连接 `ws://10.20.200.46:8765`。
- 服务端显示：`[ws] client connected: ...`。

### Step 2：系统使能（UI）

- 在 UI 面板点击 **使能** 按钮。
- 状态机进入 `ENABLED`。

### Step 3：手柄标定

- 将右手手柄举到自然参考姿态。
- 长按右手 **B** 键 5 秒。
- 服务端收到 `command=3`（`START_CALIBRATION`）。
- 5 秒后自动完成标定，状态变为 `CALIBRATED`。

### Step 4：主从同步（UI）

- 在 UI 面板点击 **同步** 按钮（或通过服务端触发）。
- 机器人缓慢移动到初始同步起点。
- 同步完成后状态变为 `SYNC_READY`。

### Step 5：进入跟随（暂用 UI 或 WS 命令）

- 当前版本：在 UI 点击 **确认跟随** 或服务端发送 `CMD_CONFIRM_FOLLOW`。
- 状态变为 `FOLLOWING`。

> 注意：左手 `X` 键（`CONFIRM_FOLLOW`）的逻辑在左手控制器开发完成后可直接使用。

### Step 6：实时控制右臂

| 操作 | 效果 |
|---|---|
| 按住右手 Grip（`>= 0.5`）+ 移动手柄 | 右臂末端实时跟随位姿 |
| 松开 Grip | 机械臂停止响应，保持当前位置 |
| 右手 Trigger（`0~1`） | 夹爪开合（`0=全开`，`1=全闭`） |
| 右手 A 键 | 自锁（机械臂冻结当前位置） |
| 再按 A 键 | 解锁（恢复跟随） |
| 右手 B 键短按 | 停止并退出跟随，状态 → `STOPPED` |
| 左右摇杆同时按下 | 软急停，状态 → `E_STOP` |

---

## 五、再次进入跟随

按右手 **B** 停止后，必须重新执行：

- Step 4（主从同步）
- Step 5（确认跟随）
- Step 6（实时控制）

---

## 六、关闭流程

1. Quest 中退出 App（或摘下头显）。
2. 服务端 `Ctrl + C` 停止。
3. 机器人会保持在最后停止位置。

---

## 七、常见问题排查

| 现象 | 原因 | 解法 |
|---|---|---|
| `[ws] listening` 但 Quest 连不上 | 防火墙或 IP 不通 | 检查 PC 防火墙，确认 Quest 和 PC 在同一网段 |
| `HRIF_Connect failed` | CPS 控制器未启动 | 启动机器人控制器后重试 |
| 移动手柄但机械臂不动 | Grip 未按住 | 确认右手 Grip 按键 `>= 0.5` |
| 机械臂突然停止 | 双摇杆误触急停 | 重新使能，并执行 Step 2 ~ 5 |
| 标定后机械臂跳动 | 标定起点偏差 | 重新标定，保持参考姿态稳定 |
