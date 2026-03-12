import asyncio
import websockets
import json

async def test():
	uri="ws://172.20.10.13:8765"
	async with websockets.connect(uri) as websocket:
		await websocket.send(json.dumps({"test": "hello"}))
		

asyncio.run(test())
