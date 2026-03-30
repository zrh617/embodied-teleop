#!/usr/bin/env python3
import asyncio
import json
import time
import websockets

msg_count = 0
last_print = time.time()

async def handler(websocket, path=None):
    global msg_count, last_print
    print("Quest connected")
    try:
        async for message in websocket:
            msg_count += 1
            now = time.time()

            try:
                data = json.loads(message)
            except Exception as e:
                print("JSON parse failed:", e)
                print("RAW:", message)
                continue

            if now - last_print >= 1.0:
                print(f"[{time.strftime('%H:%M:%S')}] recv {msg_count} msgs total, last type={data.get('type')}")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                last_print = now
    except Exception as e:
        print("Quest disconnected:", e)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server listening at ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())