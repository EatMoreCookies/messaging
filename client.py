from websockets.sync.client import connect
import json
import argparse
import threading
from models import MessageType
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument('from_client_id', type=int, nargs=1, help='from client ID')
parser.add_argument('to_client_id', type=int, nargs=1, help='to client ID')

args = parser.parse_args()

from_client_id = int(args.from_client_id[0])
to_client_id = int(args.to_client_id[0])

connection_string = "ws://localhost:8765"    

def get_messages(websocket):
    while True:
        response = websocket.recv()
        response_json = json.loads(response)
        response_body = response_json["body"]
        response_type = MessageType(response_json["type"])
        
        if response_type == MessageType.CHAT:
            print(f"\r> {response_body}")


def send_message(message: str, websocket, type: MessageType):
    message_json: dict = {
        "type": type.value,
        "to_id": to_client_id,
        "from_id": from_client_id,
        "body": message 
    }
    
    websocket.send(json.dumps(message_json))     

def run():
    websocket = connect(connection_string)
    
    message = "Connect me please"
    type = MessageType.CONNECT_ME
    
    print(f"Connecting {from_client_id} to server...")

    get_messages_thread = threading.Thread(target=get_messages, args=(websocket,))
    get_messages_thread.start()

    while True:
        send_message(message, websocket, type)
        message = input()
        type = MessageType.CHAT
        
            
run()