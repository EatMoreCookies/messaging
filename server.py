import asyncio
from websockets.server import serve
from datetime import datetime
import json
from models import MessageType

connections = {}

async def send_message(from_id: int, to_id: int, message: str, type: MessageType):
    print(f"Sending message from {from_id} to {to_id}")
    
    response_json = {
        "type": MessageType.MESSAGE_RECIEVED.value,
        "body": "Message was received by server"
    }

    response_json['body'] = message
    response_json['type'] = type.value

    if to_id in connections:
        await connections[to_id].send(json.dumps(response_json))
        print(f"Sent message from {from_id} to {to_id}")
    else:
        print(f"ID {to_id} was not found in the list of connections")

async def handle(websocket):
    async for json_string in websocket:
        message_json = json.loads(json_string)
        
        from_id = message_json['from_id']
        to_id = message_json['to_id']
        message = message_json['body']
        type = MessageType(int(message_json['type']))

        print(f"Received message {message} from {from_id} to {to_id} of type {MessageType(type)} at {datetime.now()}. {len(connections)} connections.")

        if from_id not in connections:
            print(f"Adding {from_id} to list of live connections...")

        if type == MessageType.DISCONNECT_ME:
            del connections[from_id]
            await send_message(from_id, to_id, f"User {from_id} disconnected", MessageType.MESSAGE_RECIEVED)
        else:
            connections[from_id] = websocket
            await send_message(from_id, from_id, "", MessageType.MESSAGE_RECIEVED)

            if type == MessageType.CHAT:
                await send_message(from_id, to_id, message, MessageType.CHAT)

async def main():
    print("Starting server...")
    
    async with serve(handle, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())