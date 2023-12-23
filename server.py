import asyncio
from websockets.server import serve
from datetime import datetime
import json

to_ids = []
from_ids = []

connections = {}

async def echo(websocket):
    async for json_string in websocket:
        message_json = json.loads(json_string)
        
        from_id = message_json['from_id']
        to_id = message_json['to_id']
        message = message_json['body']

        connections[from_id] = websocket

        response_msg = f"Recieved message {message} from {from_id} to {to_id} at {datetime.now()}. {len(connections)} connections."
        print(response_msg)

        if to_id in connections:
            await connections[to_id].send(message)
            
async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())