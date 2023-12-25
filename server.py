import asyncio
from websockets.server import serve
from datetime import datetime
import json
from models import MessageType

connections = {}

async def handle(websocket):
    async for json_string in websocket:
        message_json = json.loads(json_string)
        
        from_id = message_json['from_id']
        to_id = message_json['to_id']
        message = message_json['body']
        type = MessageType(int(message_json['type']))

        if from_id not in connections:
            print(f"Adding {from_id} to list of live connections...")

        connections[from_id] = websocket

        response_msg = f"Received message {message} from {from_id} to {to_id} of type {MessageType(type)} at {datetime.now()}. {len(connections)} connections."
        print(response_msg)

        response_json = {
            "type": MessageType.MESSAGE_RECIEVED.value,
            "body": "Message was received by server"
        }

        await websocket.send(json.dumps(response_json))

        if type == MessageType.CHAT and to_id in connections:
            print(f"Sending message from {from_id} to {to_id}")
            response_json['body'] = message
            response_json['type'] = MessageType.CHAT.value
            await connections[to_id].send(json.dumps(response_json))
            
async def main():
    print("Starting server...")
    
    async with serve(handle, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())