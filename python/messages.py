from dataclasses import dataclass, field
import uuid

@dataclass
class Message:
    id: str = field(init=False, default_factory=lambda: str(uuid.uuid4()))
    type: str


@dataclass
class RoomsListMsg(Message):
    type: str = field(init=False, default="rooms_list")
    rooms: list[str]


@dataclass
class CreateRoomMsg(Message):
    type: str = field(init=False, default="create_room")
    room_name: str
    state: bool


@dataclass
class ChatMsg(Message):
    type: str = field(init=False, default="chat_message")
    message: dict



@dataclass
class ChatsMsg(Message):
    type: str = field(init=False, default="chat_messages")
    messages: list


@dataclass
class IdentifiedMsg(Message):
    type: str = field(init=False, default="chat_messages")