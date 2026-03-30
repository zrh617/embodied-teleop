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
from websockets.server import WebSocketServerProtocol

from CPS import CPSClient


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


class ServoPRelay:
    def __init__(self, cfg: RelayConfig) -> None:
        self.cfg = cfg
        self.cps = CPSClient()
        self.servo_started = False
        self.initialized_to_start_pose = False
        self._origin_pos: dict | None = None  # XR pos at first frame (reference point)

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
            print(f"[relay] origin locked: {self._origin_pos}")

        dx = float(pos["x"]) - self._origin_pos["x"]
        dy = float(pos["y"]) - self._origin_pos["y"]
        dz = float(pos["z"]) - self._origin_pos["z"]

        x_mm = self.cfg.x_offset_mm + self.cfg.x_sign * dx * self.cfg.scale_mm
        y_mm = self.cfg.y_offset_mm + self.cfg.y_sign * dy * self.cfg.scale_mm
        z_mm = self.cfg.z_offset_mm + self.cfg.z_sign * dz * self.cfg.scale_mm

        rx_deg, ry_deg, rz_deg = self.quat_to_euler_xyz_deg(rot)
        rx_deg += self.cfg.rx_offset_deg
        ry_deg += self.cfg.ry_offset_deg
        rz_deg += self.cfg.rz_offset_deg

        return [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]

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
        print("[robot] moved to first pose")

    def push_pose(self, pose: list[float]) -> None:
        n_ret = self.cps.HRIF_PushServoP(
            self.cfg.box_id,
            self.cfg.robot_id,
            pose,
            ["0"] * 6,
            ["0"] * 6,
        )
        if n_ret != 0:
            raise RuntimeError(f"HRIF_PushServoP failed: {n_ret}")


class XrWsToServoPServer:
    def __init__(self, relay: ServoPRelay) -> None:
        self.relay = relay
        self.msg_count = 0

    async def run(self) -> None:
        print(f"[ws] listening on ws://{self.relay.cfg.ws_host}:{self.relay.cfg.ws_port}")
        async with websockets.serve(self.handle_client, self.relay.cfg.ws_host, self.relay.cfg.ws_port):
            await asyncio.Future()

    async def handle_client(self, websocket: WebSocketServerProtocol) -> None:
        print(f"[ws] client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                try:
                    payload = json.loads(message)
                    if payload.get("type") != "xr_controller_state":
                        continue

                    hand = payload.get(self.relay.cfg.side)
                    if not isinstance(hand, dict):
                        print(f"[warn] missing controller side={self.relay.cfg.side} in payload")
                        continue

                    pose = self.relay.xr_to_servop_pose(hand)

                    if not self.relay.initialized_to_start_pose:
                        self.relay.move_to_start_pose_once(pose)
                    self.relay.ensure_servo_started()
                    self.relay.push_pose(pose)

                    self.msg_count += 1
                    if self.msg_count == 1:
                        print(f"[push] first pose={ [round(v, 3) for v in pose] }")
                    if self.msg_count % 50 == 0:
                        p = [round(v, 3) for v in pose]
                        print(f"[push] #{self.msg_count} pose={p}")

                    seq = payload.get("seq")
                    await websocket.send(json.dumps({"ok": True, "seq": seq}))
                except Exception as e:
                    print(f"[error] process frame failed: {e}")
        finally:
            print(f"[ws] client disconnected: {websocket.remote_address}")


def parse_args() -> RelayConfig:
    parser = argparse.ArgumentParser(description="Relay XR websocket controller pose to Huayan ServoP")

    parser.add_argument("--ws-host", default="0.0.0.0")
    parser.add_argument("--ws-port", type=int, default=8765)

    parser.add_argument("--cps-ip", default="10.20.200.46")
    parser.add_argument("--cps-port", type=int, default=10003)
    parser.add_argument("--box-id", type=int, default=0)
    parser.add_argument("--robot-id", type=int, default=0)

    parser.add_argument("--side", choices=["left", "right"], default="right")

    parser.add_argument("--servo-time", type=float, default=0.02)
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
    )


def main() -> None:
    cfg = parse_args()
    relay = ServoPRelay(cfg)

    try:
        relay.connect_robot()
        server = XrWsToServoPServer(relay)
        asyncio.run(server.run())
    finally:
        relay.stop_servo()


if __name__ == "__main__":
    main()
