from websockets.sync.client import connect
import json
import argparse
import threading
from models import MessageType
import sys

parser = argparse.ArgumentParser()
parser.add_argument('from_client_id', type=int, nargs=1, help='from client ID')
parser.add_argument('to_client_id', type=int, nargs=1, help='to client ID')

args = parser.parse_args()

from_client_id = int(args.from_client_id[0])
to_client_id = int(args.to_client_id[0])

connection_string = "ws://localhost:8765"    
get_messages_exit_flag = False

should_print_response_message = lambda type: type == MessageType.CHAT or type == MessageType.DISCONNECT_SUCCESSFULL

def get_messages(websocket):
    try:
        should_get_messages = True

        while should_get_messages:
            print("Waiting for message...")
            response = websocket.recv()
            print("Recieved message")
            print(f"Exit flag = {get_messages_exit_flag}")
            response_json = json.loads(response)
            response_body = response_json["body"]
            response_type = MessageType(response_json["type"])
            
            should_get_messages = False

            if should_print_response_message(response_type):
                print(f"\r> {response_body}")
    except Exception as e:
        print(f"Exception in thread: {e}")
    
    print("Done getting messages")


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

    # read messages from server on seperate thread
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

        print(f"Disconnect request just set flag to {get_messages_exit_flag}")
        send_message(message, websocket, type)

        print("Waiting for thread to finish...")
        get_messages_thread.join()
        print("All threads finished")
        try:
            sys.exit()
        except SystemExit as e:
            print(f"Closing chat...")
            print(f"Active theads: {threading.enumerate()}")

run_client()