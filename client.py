from websockets.sync.client import connect
import json
import argparse
import threading
from models import MessageType

parser = argparse.ArgumentParser()
parser.add_argument('from_client_id', type=int, nargs=1, help='from client ID')
parser.add_argument('to_client_id', type=int, nargs=1, help='to client ID')

args = parser.parse_args()

from_client_id = int(args.from_client_id[0])
to_client_id = int(args.to_client_id[0])

connection_string = "ws://localhost:8765"    
get_messages_exit_flag = False

def get_messages(websocket):
    while not get_messages_exit_flag:
        print("Waiting for message...")
        response = websocket.recv()
        print("Recieved message")
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

def run_client():
    websocket = connect(connection_string)
    
    message = "Connect me please"
    type = MessageType.CONNECT_ME
    
    print(f"Connecting {from_client_id} to server...")

    get_messages_thread = threading.Thread(target=get_messages, args=(websocket,))
    get_messages_thread.daemon = True
    get_messages_thread.start()

    try:
        while True:
            send_message(message, websocket, type)
            message = input()
            type = MessageType.CHAT
    except KeyboardInterrupt:
        print("Disconnecting...")
        
        message = "Disconnect me please"
        type = MessageType.DISCONNECT_ME
        get_messages_exit_flag = True
        
        send_message(message, websocket, type)
        print("Waiting for thread to finish...")
        get_messages_thread.join()
        
        quit()

run_client()