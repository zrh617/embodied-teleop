#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import asyncio
import csv
import json
import math
import time
from pathlib import Path
from typing import Dict, List

import websockets


def euler_deg_to_quat(rx_deg: float, ry_deg: float, rz_deg: float) -> Dict[str, float]:
    """Convert intrinsic XYZ Euler angles (deg) to quaternion."""
    rx = math.radians(rx_deg)
    ry = math.radians(ry_deg)
    rz = math.radians(rz_deg)

    cx = math.cos(rx * 0.5)
    sx = math.sin(rx * 0.5)
    cy = math.cos(ry * 0.5)
    sy = math.sin(ry * 0.5)
    cz = math.cos(rz * 0.5)
    sz = math.sin(rz * 0.5)

    qw = cx * cy * cz + sx * sy * sz
    qx = sx * cy * cz - cx * sy * sz
    qy = cx * sy * cz + sx * cy * sz
    qz = cx * cy * sz - sx * sy * cz

    return {"x": qx, "y": qy, "z": qz, "w": qw}


def load_csv(csv_path: Path) -> List[List[float]]:
    rows: List[List[float]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, start=1):
            if len(row) < 6:
                continue
            try:
                rows.append(
                    [
                        float(row[0]),
                        float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        float(row[4]),
                        float(row[5]),
                    ]
                )
            except ValueError as e:
                raise ValueError(f"CSV row {i} parse failed: {row}") from e
    if not rows:
        raise ValueError("No valid 6-DoF rows found in csv")
    return rows


def make_controller(pos_x: float, pos_y: float, pos_z: float, quat: Dict[str, float]) -> Dict:
    return {
        "connected": True,
        "tracking_valid": True,
        "pos": {"x": pos_x, "y": pos_y, "z": pos_z},
        "rot": quat,
        "thumbstick": {"x": 0.0, "y": 0.0},
        "trigger": 0.0,
        "squeeze": 0.0,
        "buttons": {
            "primary": False,
            "secondary": False,
            "thumbstick_click": False,
            "menu": False,
            "system": False,
        },
    }


def resolve_csv_path(csv_arg: str) -> Path:
    """
    Resolve CSV path with fallback to script directory.
    This allows running the script directly from arbitrary cwd.
    """
    p = Path(csv_arg)
    if p.is_absolute() and p.exists():
        return p
    if p.exists():
        return p.resolve()

    script_dir = Path(__file__).resolve().parent
    alt = script_dir / p.name
    if alt.exists():
        return alt

    return p.resolve()


async def stream_csv(args: argparse.Namespace) -> None:
    csv_path = resolve_csv_path(args.csv)
    rows = load_csv(csv_path)

    default_quat = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
    left_default = make_controller(-0.2, 1.2, 0.4, default_quat)
    right_default = make_controller(0.2, 1.2, 0.4, default_quat)

    period = 1.0 / args.hz
    seq = args.start_seq

    print(f"Loaded {len(rows)} rows from {csv_path}")
    print(f"Sending to {args.uri} at {args.hz} Hz, target side={args.side}, loop={args.loop}")

    async with websockets.connect(
        args.uri,
        ping_interval=20,
        ping_timeout=20,
        max_size=2 * 1024 * 1024,
    ) as ws:
        while True:
            for i, row in enumerate(rows):
                row_start = time.perf_counter()
                x, y, z, rx, ry, rz = row
                quat = euler_deg_to_quat(rx, ry, rz)

                left = left_default
                right = right_default
                if args.side == "left":
                    left = make_controller(x, y, z, quat)
                else:
                    right = make_controller(x, y, z, quat)

                msg = {
                    "type": "xr_controller_state",
                    "ts_ms": int(time.time() * 1000),
                    "seq": seq,
                    "device_id": args.device_id,
                    "frame": args.frame,
                    "head": {
                        "pos": {"x": 0.0, "y": 1.5, "z": 0.2},
                        "rot": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
                    },
                    "left": left,
                    "right": right,
                }

                await ws.send(json.dumps(msg, ensure_ascii=False))
                if seq % 100 == 0:
                    print(f"sent seq={seq}, row={i + 1}/{len(rows)}")
                seq += 1

                elapsed = time.perf_counter() - row_start
                sleep_s = period - elapsed
                if sleep_s > 0:
                    await asyncio.sleep(sleep_s)

            if not args.loop:
                break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stream ServoP CSV as xr_controller_state via WebSocket"
    )
    parser.add_argument(
        "--csv",
        default="E05_ServoP_data.csv",
        help="Path to 6-column CSV (x,y,z,rx,ry,rz)",
    )
    parser.add_argument("--uri", default="ws://127.0.0.1:8765", help="WebSocket server URI")
    parser.add_argument("--hz", type=float, default=50.0, help="Send frequency")
    parser.add_argument(
        "--side",
        choices=["left", "right"],
        default="right",
        help="Which controller is driven by CSV",
    )
    parser.add_argument("--frame", default="xr_local", help="frame field")
    parser.add_argument("--device-id", default="servop_replay", help="device_id field")
    parser.add_argument("--start-seq", type=int, default=1, help="Initial seq")
    parser.add_argument("--loop", action="store_true", help="Loop replay")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asyncio.run(stream_csv(args))


if __name__ == "__main__":
    main()
