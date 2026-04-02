#!/usr/bin/env python3
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any

try:
    import rospy
    from geometry_msgs.msg import PoseStamped
    from sensor_msgs.msg import Joy
    from std_msgs.msg import Int32

    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False

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
    COMMAND_NAMES = {
        0: "NONE",
        1: "ENABLE",
        2: "DISABLE",
        3: "START_CALIBRATION",
        4: "FINISH_CALIBRATION",
        5: "START_SYNC",
        6: "CONFIRM_FOLLOW",
        7: "STOP_FOLLOW",
        8: "TOGGLE_RECORD",
        9: "TOGGLE_LOCK",
        10: "SOFT_ESTOP",
        11: "CLEAR_ESTOP",
    }

    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        self.host = host
        self.port = port
        if ROS_AVAILABLE:
            rospy.init_node("xr_ws_bridge", anonymous=True)
            self.cmd_pub = rospy.Publisher("/xr/teleop_command", Int32, queue_size=10)
            self.joy_pub = rospy.Publisher("/xr/controllers/joy", Joy, queue_size=10)
            self.left_grip_pose_pub = rospy.Publisher(
                "/xr/left_controller/grip_pose", PoseStamped, queue_size=10
            )
            self.right_grip_pose_pub = rospy.Publisher(
                "/xr/right_controller/grip_pose", PoseStamped, queue_size=10
            )
            logger.info("ROS1 Publishers initialized")

    async def run(self) -> None:
        logger.info("Starting XR WebSocket bridge on ws://%s:%s", self.host, self.port)
        async with websockets.serve(
            self.handle_client, self.host, self.port, max_size=2**20
        ):
            await asyncio.Future()

    async def handle_client(self, websocket: WebSocketServerProtocol) -> None:
        logger.info("Quest connected: %s", websocket.remote_address)
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    logger.warning(
                        "Ignoring binary frame from %s", websocket.remote_address
                    )
                    continue

                try:
                    payload = json.loads(message)
                    msg_type = payload.get("type")
                    if msg_type == "xr_controller_state":
                        state = self.parse_xr_controller_state(payload)
                        self.publish_state(state)
                        await websocket.send(json.dumps({"ok": True, "seq": state.seq}))
                    elif msg_type == "teleop_command":
                        self.publish_command(payload)
                        await websocket.send(
                            json.dumps(
                                {"ok": True, "seq": int(payload.get("seq", 0))}
                            )
                        )
                    else:
                        raise ValueError(f"unexpected type: {msg_type!r}")
                except Exception as exc:
                    logger.exception("Failed to process XR frame")
                    await websocket.send(json.dumps({"ok": False, "error": str(exc)}))
        finally:
            logger.info("Quest disconnected: %s", websocket.remote_address)

    def publish_command(self, payload: dict[str, Any]) -> None:
        cmd_id = int(payload.get("command", 0))
        cmd_name = self.COMMAND_NAMES.get(cmd_id, f"UNKNOWN_{cmd_id}")
        logger.info(
            "command seq=%s cmd=%s(%s) note=%s",
            payload.get("seq", 0),
            cmd_name,
            cmd_id,
            payload.get("note", ""),
        )
        if ROS_AVAILABLE:
            self.cmd_pub.publish(Int32(data=cmd_id))

    def parse_xr_controller_state(self, payload: dict[str, Any]) -> XrControllerState:
        return XrControllerState(
            ts_ms=int(payload["ts_ms"]),
            seq=int(payload["seq"]),
            head=HeadState(
                pos=self.parse_vec3(payload["head"]["pos"]),
                rot=self.parse_quat(payload["head"]["rot"]),
            ),
            left=self.parse_controller(payload["left"]),
            right=self.parse_controller(payload["right"]),
        )

    def parse_controller(self, payload: dict[str, Any]) -> ControllerState:
        return ControllerState(
            connected=bool(payload["connected"]),
            pos=self.parse_vec3(payload["pos"]),
            rot=self.parse_quat(payload["rot"]),
            thumbstick=self.parse_vec2(
                payload.get("thumbstick", {"x": 0.0, "y": 0.0})
            ),
            trigger=float(payload.get("trigger", 0.0)),
            squeeze=float(payload.get("squeeze", 0.0)),
            buttons=self.parse_buttons(payload.get("buttons", {})),
        )

    @staticmethod
    def parse_vec2(payload: dict[str, Any]) -> Vec2:
        return Vec2(x=float(payload["x"]), y=float(payload["y"]))

    @staticmethod
    def parse_vec3(payload: dict[str, Any]) -> Vec3:
        return Vec3(
            x=float(payload["x"]), y=float(payload["y"]), z=float(payload["z"])
        )

    @staticmethod
    def parse_quat(payload: dict[str, Any]) -> Quat:
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

    @staticmethod
    def _to_pose_stamped(state: ControllerState) -> PoseStamped:
        msg = PoseStamped()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "xr_local"
        msg.pose.position.x = state.pos.x
        msg.pose.position.y = state.pos.y
        msg.pose.position.z = state.pos.z
        msg.pose.orientation.x = state.rot.x
        msg.pose.orientation.y = state.rot.y
        msg.pose.orientation.z = state.rot.z
        msg.pose.orientation.w = state.rot.w
        return msg

    def publish_state(self, state: XrControllerState) -> None:
        logger.info(
            "seq=%s left(grip=%.2f trig=%.2f) right(grip=%.2f trig=%.2f)",
            state.seq,
            state.left.squeeze,
            state.left.trigger,
            state.right.squeeze,
            state.right.trigger,
        )
        if ROS_AVAILABLE:
            joy_msg = Joy()
            joy_msg.header.stamp = rospy.Time.now()
            joy_msg.header.frame_id = "quest_controllers"
            # Mapping: [L_trig, L_sqz, R_trig, R_sqz, L_ts_x, L_ts_y, R_ts_x, R_ts_y]
            joy_msg.axes = [
                state.left.trigger,
                state.left.squeeze,
                state.right.trigger,
                state.right.squeeze,
                state.left.thumbstick.x,
                state.left.thumbstick.y,
                state.right.thumbstick.x,
                state.right.thumbstick.y,
            ]
            # Mapping: [X, Y, A, B, L_ts_click, R_ts_click, Menu]
            joy_msg.buttons = [
                int(state.left.buttons.primary),
                int(state.left.buttons.secondary),
                int(state.right.buttons.primary),
                int(state.right.buttons.secondary),
                int(state.left.buttons.thumbstick_click),
                int(state.right.buttons.thumbstick_click),
                int(state.left.buttons.menu),
            ]
            self.joy_pub.publish(joy_msg)

            if state.left.connected:
                self.left_grip_pose_pub.publish(self._to_pose_stamped(state.left))
            if state.right.connected:
                self.right_grip_pose_pub.publish(self._to_pose_stamped(state.right))


def main() -> None:
    bridge = XrWsBridge(host="0.0.0.0", port=8765)
    asyncio.run(bridge.run())


if __name__ == "__main__":
    main()
