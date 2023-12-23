from websockets.sync.client import connect
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('from_client_id', type=int, nargs=1, help='from client ID')
parser.add_argument('to_client_id', type=int, nargs=1, help='to client ID')

args = parser.parse_args()

from_client_id = int(args.from_client_id[0])
to_client_id = int(args.to_client_id[0])

def send_message_to_server(msg: str):
    with connect("ws://localhost:8765") as websocket:
        message_json: dict = {
            "to_id": to_client_id,
            "from_id": from_client_id,
            "body": msg 
        }

        websocket.send(json.dumps(message_json))
        response = websocket.recv()

        print(f"< {response}")

while True:
    message = input("> ")
    send_message_to_server(message)