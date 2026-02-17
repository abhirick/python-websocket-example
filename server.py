# server.py
import asyncio
import websockets
import json
from datetime import datetime

PORT = 8765

async def handler(ws):
    client = ws.remote_address
    
    # correct way in websockets 13+
    path = ws.request.path

    print(f"Client connected: {client}, path={path}")

    await ws.send(json.dumps({
        "type": "welcome",
        "message": "Connected to Python WebSocket server",
        "path": path,
        "time": datetime.utcnow().isoformat()
    }))

    try:
        async for message in ws:
            print(f"Received: {message}")

            response = {
                "type": "echo",
                "received": message,
                "time": datetime.utcnow().isoformat()
            }

            await ws.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"WebSocket server running on ws://localhost:{PORT}")
        await asyncio.Future()

asyncio.run(main())
