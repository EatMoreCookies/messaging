import asyncio
from websockets.server import serve
from datetime import datetime
import json

connections = {}

async def echo(websocket):
    async for json_string in websocket:
        message_json = json.loads(json_string)
        
        from_id = message_json['from_id']
        to_id = message_json['to_id']
        message = message_json['body']
        type = message_json['type']

        connections[from_id] = websocket

        response_msg = f"Recieved message {message} from {from_id} to {to_id} at {datetime.now()}. {len(connections)} connections."
        print(response_msg)

        # await websocket.send("__message__received__")

        if to_id in connections:
            print(f"Sending message from {from_id} to {to_id}")
            await connections[to_id].send(message)
            
async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())