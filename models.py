from enum import Enum

class MessageType(Enum):
    CHAT = 0
    CONNECT_ME = 1
    MESSAGE_RECIEVED = 2
    DISCONNECT_ME = 3
