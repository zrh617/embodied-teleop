#!/usr/bin/env python3
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any

import websockets
from websockets.server import WebSocketServerProtocol

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("xr_ws_bridge")


@dataclass
class Vec2:
    x: float
    y: float


@dataclass
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Quat:
    x: float
    y: float
    z: float
    w: float


@dataclass
class Buttons:
    primary: bool = False
    secondary: bool = False
    thumbstick_click: bool = False
    menu: bool = False
    system: bool = False


@dataclass
class HeadState:
    pos: Vec3
    rot: Quat


@dataclass
class ControllerState:
    connected: bool
    pos: Vec3
    rot: Quat
    thumbstick: Vec2
    trigger: float
    squeeze: float
    buttons: Buttons


@dataclass
class XrControllerState:
    ts_ms: int
    seq: int
    head: HeadState
    left: ControllerState
    right: ControllerState


class XrWsBridge:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        self.host = host
        self.port = port

    async def run(self) -> None:
        logger.info("Starting XR WebSocket bridge on ws://%s:%s", self.host, self.port)
        async with websockets.serve(self.handle_client, self.host, self.port, max_size=2**20):
            await asyncio.Future()

    async def handle_client(self, websocket: WebSocketServerProtocol) -> None:
        logger.info("Quest connected: %s", websocket.remote_address)
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    logger.warning("Ignoring binary frame from %s", websocket.remote_address)
                    continue

                try:
                    payload = json.loads(message)
                    state = self.parse_xr_controller_state(payload)
                    self.publish_state(state)
                    await websocket.send(json.dumps({"ok": True, "seq": state.seq}))
                except Exception as exc:
                    logger.exception("Failed to process XR frame")
                    await websocket.send(json.dumps({"ok": False, "error": str(exc)}))
        finally:
            logger.info("Quest disconnected: %s", websocket.remote_address)

    def parse_xr_controller_state(self, payload: dict[str, Any]) -> XrControllerState:
        if payload.get("type") != "xr_controller_state":
            raise ValueError(f"unexpected type: {payload.get('type')!r}")

        return XrControllerState(
            ts_ms=int(payload["ts_ms"]),
            seq=int(payload["seq"]),
            head=HeadState(
                pos=self.parse_vec3(payload["head"]["pos"], "head.pos"),
                rot=self.parse_quat(payload["head"]["rot"], "head.rot"),
            ),
            left=self.parse_controller(payload["left"], "left"),
            right=self.parse_controller(payload["right"], "right"),
        )

    def parse_controller(self, payload: dict[str, Any], prefix: str) -> ControllerState:
        return ControllerState(
            connected=bool(payload["connected"]),
            pos=self.parse_vec3(payload["pos"], f"{prefix}.pos"),
            rot=self.parse_quat(payload["rot"], f"{prefix}.rot"),
            thumbstick=self.parse_vec2(payload.get("thumbstick", {}), f"{prefix}.thumbstick"),
            trigger=float(payload.get("trigger", 0.0)),
            squeeze=float(payload.get("squeeze", 0.0)),
            buttons=self.parse_buttons(payload.get("buttons", {})),
        )

    @staticmethod
    def parse_vec2(payload: dict[str, Any], field: str) -> Vec2:
        return Vec2(x=float(payload["x"]), y=float(payload["y"]))

    @staticmethod
    def parse_vec3(payload: dict[str, Any], field: str) -> Vec3:
        return Vec3(x=float(payload["x"]), y=float(payload["y"]), z=float(payload["z"]))

    @staticmethod
    def parse_quat(payload: dict[str, Any], field: str) -> Quat:
        return Quat(
            x=float(payload["x"]),
            y=float(payload["y"]),
            z=float(payload["z"]),
            w=float(payload["w"]),
        )

    @staticmethod
    def parse_buttons(payload: dict[str, Any]) -> Buttons:
        return Buttons(
            primary=bool(payload.get("primary", False)),
            secondary=bool(payload.get("secondary", False)),
            thumbstick_click=bool(payload.get("thumbstick_click", False)),
            menu=bool(payload.get("menu", False)),
            system=bool(payload.get("system", False)),
        )

    def publish_state(self, state: XrControllerState) -> None:
        # Replace these logging calls with ROS publishers on the Ubuntu machine.
        logger.info(
            "seq=%s ts_ms=%s head=(%.3f, %.3f, %.3f) left.connected=%s right.connected=%s",
            state.seq,
            state.ts_ms,
            state.head.pos.x,
            state.head.pos.y,
            state.head.pos.z,
            state.left.connected,
            state.right.connected,
        )


def main() -> None:
    bridge = XrWsBridge(host="0.0.0.0", port=8765)
    asyncio.run(bridge.run())


if __name__ == "__main__":
    main()
