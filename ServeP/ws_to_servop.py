#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Receive XR controller state from WebSocket and relay to Huayan ServoP.

Message format expected (from app):
  type = "xr_controller_state"
  right/left.pos = {x,y,z} in meters
  right/left.rot = quaternion {x,y,z,w}

Output to robot:
  [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
"""

import argparse
import asyncio
import json
import math
from dataclasses import dataclass
from typing import Any, Dict

import websockets
from websockets.exceptions import ConnectionClosed

try:
    import rospy
    from fleximind_remote.msg import TeleopCommand

    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False

from CPS import CPSClient


CMD_NONE = 0
CMD_ENABLE = 1
CMD_DISABLE = 2
CMD_START_CALIBRATION = 3
CMD_FINISH_CALIBRATION = 4
CMD_START_SYNC = 5
CMD_CONFIRM_FOLLOW = 6
CMD_STOP_FOLLOW = 7
CMD_TOGGLE_RECORD = 8
CMD_TOGGLE_LOCK = 9
CMD_SOFT_ESTOP = 10
CMD_CLEAR_ESTOP = 11

COMMAND_NAMES = {
    CMD_NONE: "NONE",
    CMD_ENABLE: "ENABLE",
    CMD_DISABLE: "DISABLE",
    CMD_START_CALIBRATION: "START_CALIBRATION",
    CMD_FINISH_CALIBRATION: "FINISH_CALIBRATION",
    CMD_START_SYNC: "START_SYNC",
    CMD_CONFIRM_FOLLOW: "CONFIRM_FOLLOW",
    CMD_STOP_FOLLOW: "STOP_FOLLOW",
    CMD_TOGGLE_RECORD: "TOGGLE_RECORD",
    CMD_TOGGLE_LOCK: "TOGGLE_LOCK",
    CMD_SOFT_ESTOP: "SOFT_ESTOP",
    CMD_CLEAR_ESTOP: "CLEAR_ESTOP",
}


@dataclass
class TeleopRuntimeState:
    enabled: bool = True
    calibrated: bool = True
    sync_ready: bool = True
    following: bool = True
    recording: bool = False
    locked: bool = False
    estop: bool = False


@dataclass
class RelayConfig:
    ws_host: str
    ws_port: int
    cps_ip: str
    cps_port: int
    box_id: int
    robot_id: int
    side: str
    servo_time: float
    lookahead_time: float
    scale_mm: float
    x_sign: float
    y_sign: float
    z_sign: float
    x_offset_mm: float
    y_offset_mm: float
    z_offset_mm: float
    rx_offset_deg: float
    ry_offset_deg: float
    rz_offset_deg: float
    tcp_name: str
    ucs_name: str
    grip_threshold: float
    x_min_mm: float
    x_max_mm: float
    y_min_mm: float
    y_max_mm: float
    z_min_mm: float
    z_max_mm: float


class ServoPRelay:
    def __init__(self, cfg: RelayConfig) -> None:
        self.cfg = cfg
        self.cps = CPSClient()
        self.servo_started = False
        self.initialized_to_start_pose = False
        self._origin_pos: dict | None = None  # XR pos at first frame (reference point)
        self._fixed_rpy_deg: tuple[float, float, float] | None = None
        self._last_sent_pose: list[float] | None = None
        self.last_gripper_cmd: float = 0.0  # Track last gripper command to avoid spam
        self.grip_enable_threshold = cfg.grip_threshold
        self._latest_pose: list[float] | None = None  # Most recent pose to push
        self._push_fail_count: int = 0
        self._block_target_updates: bool = False  # Latch after unreachable target (20031)
        self._clamp_warn_count: int = 0

    def connect_robot(self) -> None:
        n_ret = self.cps.HRIF_Connect(self.cfg.box_id, self.cfg.cps_ip, self.cfg.cps_port)
        if n_ret != 0:
            raise RuntimeError(f"HRIF_Connect failed: {n_ret}")
        print(f"[robot] connected to {self.cfg.cps_ip}:{self.cfg.cps_port}")

    def ensure_servo_started(self) -> None:
        if self.servo_started:
            return
        n_ret = self.cps.HRIF_StartServo(
            self.cfg.box_id,
            self.cfg.robot_id,
            self.cfg.servo_time,
            self.cfg.lookahead_time,
        )
        if n_ret != 0:
            raise RuntimeError(f"HRIF_StartServo failed: {n_ret}")
        self.servo_started = True
        print(
            f"[robot] ServoP started: servo_time={self.cfg.servo_time}s "
            f"lookahead={self.cfg.lookahead_time}s"
        )

    def stop_servo(self) -> None:
        if not self.servo_started:
            return
        # CPS.py in this repo does not expose HRIF_EndServo/HRIF_StopServo.
        # Keep local state only; robot-side stop should be handled by your controller policy.
        self.servo_started = False

    @staticmethod
    def quat_to_euler_xyz_deg(q: Dict[str, float]) -> tuple[float, float, float]:
        """Quaternion -> intrinsic XYZ Euler (degrees)."""
        x = float(q["x"])
        y = float(q["y"])
        z = float(q["z"])
        w = float(q["w"])

        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        rx = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1.0:
            ry = math.copysign(math.pi / 2.0, sinp)
        else:
            ry = math.asin(sinp)

        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        rz = math.atan2(siny_cosp, cosy_cosp)

        return math.degrees(rx), math.degrees(ry), math.degrees(rz)

    def xr_to_servop_pose(self, hand: Dict[str, Any]) -> list[float]:
        pos = hand["pos"]
        rot = hand["rot"]

        # Use XR position as a delta from the first received pose so that the
        # robot always starts at its home pose (offsets) regardless of where
        # the controller happens to be in world space.
        if self._origin_pos is None:
            self._origin_pos = {
                "x": float(pos["x"]),
                "y": float(pos["y"]),
                "z": float(pos["z"]),
            }
            self._fixed_rpy_deg = (
                self.cfg.rx_offset_deg,
                self.cfg.ry_offset_deg,
                self.cfg.rz_offset_deg,
            )
            print(f"[relay] origin locked: {self._origin_pos}")
            print(f"[relay] fixed rpy: {[round(v, 3) for v in self._fixed_rpy_deg]}")

        dx = float(pos["x"]) - self._origin_pos["x"]
        dy = float(pos["y"]) - self._origin_pos["y"]
        dz = float(pos["z"]) - self._origin_pos["z"]

        x_mm = self.cfg.x_offset_mm + self.cfg.x_sign * dx * self.cfg.scale_mm
        y_mm = self.cfg.y_offset_mm + self.cfg.y_sign * dy * self.cfg.scale_mm
        z_mm = self.cfg.z_offset_mm + self.cfg.z_sign * dz * self.cfg.scale_mm

        # Keep a stable TCP orientation in demo mode to avoid ServoP IK reject (40071).
        if self._fixed_rpy_deg is None:
            rx_deg = self.cfg.rx_offset_deg
            ry_deg = self.cfg.ry_offset_deg
            rz_deg = self.cfg.rz_offset_deg
        else:
            rx_deg, ry_deg, rz_deg = self._fixed_rpy_deg

        return self.clamp_workspace([x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg])

    def clamp_workspace(self, pose: list[float]) -> list[float]:
        x, y, z, rx, ry, rz = pose
        cx = min(max(x, self.cfg.x_min_mm), self.cfg.x_max_mm)
        cy = min(max(y, self.cfg.y_min_mm), self.cfg.y_max_mm)
        cz = min(max(z, self.cfg.z_min_mm), self.cfg.z_max_mm)
        if cx != x or cy != y or cz != z:
            self._clamp_warn_count += 1
            if self._clamp_warn_count <= 3 or self._clamp_warn_count % 20 == 0:
                print(
                    f"[guard] workspace clamped #{self._clamp_warn_count}: "
                    f"raw={[round(x,3), round(y,3), round(z,3)]} -> "
                    f"clamped={[round(cx,3), round(cy,3), round(cz,3)]}"
                )
        return [cx, cy, cz, rx, ry, rz]

    def move_to_start_pose_once(self, pose: list[float]) -> None:
        if self.initialized_to_start_pose:
            return

        # Convert first Cartesian pose to joint target, then MoveJ once to reduce sudden jump.
        print(f"[robot] IK for start pose: {[round(v, 3) for v in pose]}")
        result: list[Any] = []
        n_ret = self.cps.HRIF_GetInverseKin(
            self.cfg.box_id,
            self.cfg.robot_id,
            pose,
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            result,
        )
        if n_ret != 0:
            print(f"[warn] HRIF_GetInverseKin failed (code={n_ret}) for pose {[round(v,3) for v in pose]}. Skipping init MoveJ.")
            self.initialized_to_start_pose = True
            return

        n_ret = self.cps.HRIF_MoveJ(
            self.cfg.box_id,
            self.cfg.robot_id,
            [0, 0, 0, 0, 0, 0],
            result,
            self.cfg.tcp_name,
            self.cfg.ucs_name,
            50,
            360,
            50,
            1,
            0,
            0,
            0,
            "0",
        )
        if n_ret != 0:
            raise RuntimeError(f"HRIF_MoveJ failed: {n_ret}")

        done: list[Any] = []
        self.cps.HRIF_IsMotionDone(self.cfg.box_id, self.cfg.robot_id, done)
        while not done[0]:
            self.cps.HRIF_IsMotionDone(self.cfg.box_id, self.cfg.robot_id, done)

        self.initialized_to_start_pose = True
        self._last_sent_pose = pose.copy()
        print("[robot] moved to first pose")

    def update_latest_pose(self, pose: list[float]) -> None:
        """Update desired ServoP target pose (non-blocking)."""
        if self._block_target_updates:
            return
        self._latest_pose = pose

    def unblock_target_updates(self) -> None:
        self._block_target_updates = False

    def push_latest_pose(self) -> bool:
        """Push latest pose once. Should be called at fixed servo_time interval."""
        if self._latest_pose is None:
            return False

        pose = self._latest_pose.copy()

        # Clamp each sent step to avoid controller rejecting large jumps (e.g. 40071/20031).
        if self._last_sent_pose is not None:
            max_step_mm = 6.0
            for i in range(3):
                delta = pose[i] - self._last_sent_pose[i]
                if delta > max_step_mm:
                    pose[i] = self._last_sent_pose[i] + max_step_mm
                elif delta < -max_step_mm:
                    pose[i] = self._last_sent_pose[i] - max_step_mm

        n_ret = self.cps.HRIF_PushServoP(
            self.cfg.box_id,
            self.cfg.robot_id,
            pose,
            ["0"] * 6,
            ["0"] * 6,
        )
        if n_ret != 0:
            self._push_fail_count += 1
            if n_ret == 20031:
                # Target is not reachable now. Hold current reachable pose and stop accepting new targets
                # until operator re-confirms follow.
                self._block_target_updates = True
                if self._last_sent_pose is not None:
                    self._latest_pose = self._last_sent_pose.copy()
            if n_ret == 40071:
                # Servo task likely stopped on controller side; force re-start on next tick.
                self.servo_started = False
            if self._push_fail_count <= 3 or self._push_fail_count % 10 == 0:
                err = []
                self.cps.HRIF_GetErrorCodeStr(self.cfg.box_id, n_ret, err)
                err_text = err[0] if err else ""
                print(f"[warn] HRIF_PushServoP failed: {n_ret} (count={self._push_fail_count}) {err_text}")
                if n_ret == 20031:
                    print("[warn] target update latched due to unreachable pose; press CONFIRM_FOLLOW to resume")
            return False

        self._push_fail_count = 0
        self._last_sent_pose = pose.copy()
        return True

    def reset_reference(self) -> None:
        self._origin_pos = None
        self._fixed_rpy_deg = None
        self._last_sent_pose = None

    def set_gripper(self, trigger: float) -> None:
        """
        v2 spec: Trigger (0~1) controls gripper open/close.
        Only send if changed significantly to avoid spam.
        """
        if abs(trigger - self.last_gripper_cmd) < 0.05:
            return  # Ignore small changes
        self.last_gripper_cmd = trigger
        # TODO: implement actual gripper command via CPS API
        # For now, just log it
        print(f"[gripper] trigger={trigger:.2f}")


class XrWsToServoPServer:
    def __init__(self, relay: ServoPRelay, forward_record_topic: bool = False) -> None:
        self.relay = relay
        self.msg_count = 0
        self.teleop = TeleopRuntimeState()
        self.teleop_cmd_pub = None

        if forward_record_topic and ROS_AVAILABLE:
            try:
                if not rospy.core.is_initialized():
                    rospy.init_node("servop_ws_bridge", anonymous=True, disable_signals=True)
                self.teleop_cmd_pub = rospy.Publisher("/vr/teleop_command", TeleopCommand, queue_size=20)
                print("[ros] publisher ready: /vr/teleop_command")
            except Exception as e:
                print(f"[ros] init failed: {e}")

    def publish_teleop_topic(self, cmd: int) -> None:
        if not self.teleop_cmd_pub:
            return

        msg = TeleopCommand()
        msg.header.stamp = rospy.Time.now()
        msg.source = TeleopCommand.SRC_VR
        msg.command_type = cmd
        msg.note = COMMAND_NAMES.get(cmd, f"cmd_{cmd}")
        self.teleop_cmd_pub.publish(msg)

    async def servo_push_loop(self) -> None:
        """Dedicated servo loop: keep pushing at fixed interval."""
        while True:
            try:
                if self.teleop.estop:
                    await asyncio.sleep(self.relay.cfg.servo_time)
                    continue

                if self.teleop.enabled and self.teleop.calibrated and self.teleop.sync_ready and self.teleop.following and not self.teleop.locked:
                    if self.relay.initialized_to_start_pose and self.relay._latest_pose is not None:
                        self.relay.ensure_servo_started()
                        sent = self.relay.push_latest_pose()
                        if sent:
                            self.msg_count += 1
                            if self.msg_count == 1:
                                p = [round(v, 3) for v in self.relay._latest_pose]
                                print(f"[push] first pose={p}")
                            elif self.msg_count % 50 == 0:
                                p = [round(v, 3) for v in self.relay._latest_pose]
                                print(f"[push] #{self.msg_count} pose={p}")
            except Exception as e:
                print(f"[error] servo loop failed: {e}")

            await asyncio.sleep(self.relay.cfg.servo_time)

    async def run(self) -> None:
        print(f"[ws] listening on ws://{self.relay.cfg.ws_host}:{self.relay.cfg.ws_port}")
        asyncio.create_task(self.servo_push_loop())
        async with websockets.serve(self.handle_client, self.relay.cfg.ws_host, self.relay.cfg.ws_port):
            await asyncio.Future()

    def can_follow(self) -> bool:
        return (
            self.teleop.enabled
            and self.teleop.calibrated
            and self.teleop.sync_ready
            and self.teleop.following
            and not self.teleop.locked
            and not self.teleop.estop
        )

    def print_motion_gate(self, hand: Dict[str, Any]) -> None:
        grip = float(hand.get("grip", 0.0))
        print(
            f"[gate] follow={self.teleop.following} lock={self.teleop.locked} estop={self.teleop.estop} "
            f"grip={grip:.2f} threshold={self.relay.grip_enable_threshold:.2f}"
        )

    def handle_command(self, cmd: int) -> None:
        if cmd == CMD_ENABLE:
            self.teleop.enabled = True
            print("[fsm] ENABLED")
            return
        if cmd == CMD_DISABLE:
            self.teleop = TeleopRuntimeState(enabled=False)
            print("[fsm] IDLE (disabled)")
            return
        if cmd == CMD_START_CALIBRATION:
            if not self.teleop.following:
                self.teleop.calibrated = False
                self.relay.reset_reference()
                print("[fsm] CALIBRATING")
            return
        if cmd == CMD_FINISH_CALIBRATION:
            self.teleop.calibrated = True
            # Demo bridge has no dedicated sync service, so mark sync-ready directly.
            self.teleop.sync_ready = True
            print("[fsm] CALIBRATED -> SYNC_READY")
            return
        if cmd == CMD_START_SYNC:
            if self.teleop.calibrated:
                self.teleop.sync_ready = True
                print("[fsm] SYNC_READY")
            return
        if cmd == CMD_CONFIRM_FOLLOW:
            # Demo bridge policy: allow quick resume without strict re-sync.
            if self.teleop.enabled and not self.teleop.estop:
                self.teleop.calibrated = True
                self.teleop.sync_ready = True
                self.teleop.following = True
                self.teleop.locked = False
                self.relay.unblock_target_updates()
                print("[fsm] FOLLOWING")
            else:
                print("[fsm] CONFIRM_FOLLOW rejected")
            return
        if cmd == CMD_STOP_FOLLOW:
            self.teleop.following = False
            self.teleop.recording = False
            self.teleop.locked = False
            print("[fsm] STOPPED")
            return
        if cmd == CMD_TOGGLE_RECORD:
            if self.teleop.following and not self.teleop.locked:
                self.teleop.recording = not self.teleop.recording
                print(f"[fsm] RECORDING={self.teleop.recording}")
            return
        if cmd == CMD_TOGGLE_LOCK:
            if self.teleop.following:
                self.teleop.locked = not self.teleop.locked
                print(f"[fsm] LOCKED={self.teleop.locked}")
            return
        if cmd == CMD_SOFT_ESTOP:
            self.teleop.estop = True
            self.teleop.following = False
            self.teleop.recording = False
            self.teleop.locked = False
            print("[fsm] E_STOP")
            return
        if cmd == CMD_CLEAR_ESTOP:
            self.teleop.estop = False
            print("[fsm] E_STOP cleared")

    async def handle_client(self, websocket, path=None) -> None:
        print(f"[ws] client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                try:
                    payload = json.loads(message)
                    msg_type = payload.get("type")

                    # ── Handle teleop_command messages ─────────────────────────
                    if msg_type == "teleop_command":
                        cmd = int(payload.get("command", CMD_NONE))
                        cmd_name = COMMAND_NAMES.get(cmd, f"UNKNOWN_{cmd}")
                        print(f"[cmd] received {cmd_name} ({cmd})")

                        if cmd == CMD_TOGGLE_RECORD:
                            self.publish_teleop_topic(cmd)
                            print("[ros] forwarded TOGGLE_RECORD -> /vr/teleop_command")

                        self.handle_command(cmd)
                        await websocket.send(json.dumps({"ok": True, "seq": payload.get("seq", 0)}))
                        continue

                    # ── Handle xr_controller_state messages ────────────────────
                    if msg_type != "xr_controller_state":
                        continue

                    hand = payload.get(self.relay.cfg.side)
                    if not isinstance(hand, dict):
                        print(f"[warn] missing controller side={self.relay.cfg.side}")
                        continue

                    # v2 spec: must satisfy state machine gate + Grip enable
                    grip = float(hand.get("grip", 0.0))
                    grip_enabled = grip >= self.relay.grip_enable_threshold
                    allow_motion = self.can_follow() and grip_enabled

                    if allow_motion:
                        pose = self.relay.xr_to_servop_pose(hand)
                        if not self.relay.initialized_to_start_pose:
                            self.relay.move_to_start_pose_once(pose)
                        self.relay.update_latest_pose(pose)
                    else:
                        if self.msg_count == 0 or self.msg_count % 50 == 0:
                            self.print_motion_gate(hand)

                    # v2 spec: Trigger controls gripper
                    trigger = float(hand.get("trigger", 0.0))
                    self.relay.set_gripper(trigger)

                    seq = payload.get("seq")
                    await websocket.send(json.dumps({"ok": True, "seq": seq}))

                except Exception as e:
                    print(f"[error] process frame failed: {e}")
        except ConnectionClosed as e:
            # Quest app may be killed or Wi-Fi may drop; this is expected occasionally.
            print(f"[ws] client closed ({e.code}): {e.reason or 'no reason'}")
        finally:
            print(f"[ws] client disconnected: {websocket.remote_address}")


def parse_args() -> tuple[RelayConfig, bool]:
    parser = argparse.ArgumentParser(description="Relay XR websocket controller pose to Huayan ServoP")

    parser.add_argument("--ws-host", default="0.0.0.0")
    parser.add_argument("--ws-port", type=int, default=8765)

    parser.add_argument("--cps-ip", default="10.20.200.46")
    parser.add_argument("--cps-port", type=int, default=10003)
    parser.add_argument("--box-id", type=int, default=0)
    parser.add_argument("--robot-id", type=int, default=0)

    parser.add_argument("--side", choices=["left", "right"], default="right")

    parser.add_argument("--servo-time", type=float, default=0.04)
    parser.add_argument("--lookahead-time", type=float, default=0.2)

    parser.add_argument("--scale-mm", type=float, default=1000.0, help="position scale, m->mm default 1000")
    parser.add_argument("--x-sign", type=float, default=1.0)
    parser.add_argument("--y-sign", type=float, default=1.0)
    parser.add_argument("--z-sign", type=float, default=1.0)

    parser.add_argument("--x-offset-mm", type=float, default=420.0)
    parser.add_argument("--y-offset-mm", type=float, default=445.0)
    parser.add_argument("--z-offset-mm", type=float, default=180.0)

    parser.add_argument("--rx-offset-deg", type=float, default=180.0)
    parser.add_argument("--ry-offset-deg", type=float, default=0.0)
    parser.add_argument("--rz-offset-deg", type=float, default=-90.0)

    parser.add_argument("--tcp-name", default="TCP")
    parser.add_argument("--ucs-name", default="Base")
    parser.add_argument("--grip-threshold", type=float, default=0.2)

    # Workspace soft limits (mm): prevent unreachable pose jumps (20031)
    parser.add_argument("--x-min-mm", type=float, default=300.0)
    parser.add_argument("--x-max-mm", type=float, default=520.0)
    parser.add_argument("--y-min-mm", type=float, default=250.0)
    parser.add_argument("--y-max-mm", type=float, default=620.0)
    parser.add_argument("--z-min-mm", type=float, default=20.0)
    parser.add_argument("--z-max-mm", type=float, default=420.0)
    parser.add_argument("--forward-record-topic", action="store_true", help="Forward TOGGLE_RECORD to /vr/teleop_command")

    a = parser.parse_args()
    return RelayConfig(
        ws_host=a.ws_host,
        ws_port=a.ws_port,
        cps_ip=a.cps_ip,
        cps_port=a.cps_port,
        box_id=a.box_id,
        robot_id=a.robot_id,
        side=a.side,
        servo_time=a.servo_time,
        lookahead_time=a.lookahead_time,
        scale_mm=a.scale_mm,
        x_sign=a.x_sign,
        y_sign=a.y_sign,
        z_sign=a.z_sign,
        x_offset_mm=a.x_offset_mm,
        y_offset_mm=a.y_offset_mm,
        z_offset_mm=a.z_offset_mm,
        rx_offset_deg=a.rx_offset_deg,
        ry_offset_deg=a.ry_offset_deg,
        rz_offset_deg=a.rz_offset_deg,
        tcp_name=a.tcp_name,
        ucs_name=a.ucs_name,
        grip_threshold=a.grip_threshold,
        x_min_mm=a.x_min_mm,
        x_max_mm=a.x_max_mm,
        y_min_mm=a.y_min_mm,
        y_max_mm=a.y_max_mm,
        z_min_mm=a.z_min_mm,
        z_max_mm=a.z_max_mm,
    ), a.forward_record_topic


def main() -> None:
    cfg, forward_record_topic = parse_args()
    relay = ServoPRelay(cfg)

    try:
        relay.connect_robot()
        server = XrWsToServoPServer(relay, forward_record_topic=forward_record_topic)
        asyncio.run(server.run())
    finally:
        relay.stop_servo()


if __name__ == "__main__":
    main()
