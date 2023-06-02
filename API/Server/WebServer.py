import asyncio
import websockets
import json

async def server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(data)

start_server = websockets.serve(server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
