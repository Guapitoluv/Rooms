from websockets.asyncio.server import serve, ServerConnection
from dataclasses import asdict, is_dataclass
from typing import Any
import asyncio
import json

from models.models import Room, TextMessage
from models.room_manager import RoomManager
from models.session_manager import SessionManager

from messages import (
    CreateRoomMsg,
    RoomsListMsg,
    ChatMsg,
    ChatsMsg,
    IdentifiedMsg
)


class Server:
    def __init__(self):
        
        self.room_manager: RoomManager = RoomManager()
        self.session_manager: SessionManager = SessionManager()
        
        self.handlers = {
            "identify": self.handle_identify,
            "request_rooms_list": self.handle_request_rooms_list,
            "create_room": self.handle_create_room,
            "enter_room": self.handle_enter_room,
            "request_chat_messages": self.handle_request_chat_messages,
            "chat_message": self.handle_chat_message,
        }
    
    
    async def send_msg(self, ws, msg) -> None:
        """
        Supports:
        - dataclasses
        - dict
        - regular objects (__dict__)
        """
    
        if is_dataclass(msg):
            payload = asdict(msg)
    
        elif hasattr(msg, "__dict__"):
            payload = vars(msg)
    
        else:
            payload = msg
    
        try:
            json.dumps(payload)
        except (TypeError, OverflowError) as e:
            raise TypeError("Message is not JSON serializable") from e
    
        print(f"sending message of type {payload.get('type', '<unknown>')}")
    
        await ws.send(json.dumps(payload))
    
    
    async def handler(self, ws) -> None:
        try:
            async for raw in ws:
                data: dict[str, Any] = json.loads(raw)
                print(f"received message of type '{data.get('type')}'")
                handler = self.handlers.get(data.get("type"))

                if handler is not None:
                    await handler(ws, data)

        except Exception as e:
            print(e)
        
        finally:
            await self.disconnect(ws)
    
    
    async def disconnect(self, ws) -> None:
        user_name, room_name = self.session_manager.disconnect(ws)
        
        if (
            user_name is None
            or room_name is None
        ):
            return

        self.room_manager.leave(room_name, user_name)
        
        room: Room = self.room_manager.get(room_name)
        
        if (
            not room.empty
            and not room.permanent
        ):
            self.room_manager.remove(room_name)
    
    
    async def handle_identify(self, ws, data):
        self.session_manager.identify(data["user_name"], ws)

        await self.send_msg(ws, IdentifiedMsg())
    
    
    async def handle_request_rooms_list(self, ws, data):
        await self.send_msg(
            ws,
            RoomsListMsg(self.room_manager.to_dict())
        )
    
    
    async def handle_create_room(self, ws, data):
        room_name = data["room_name"]

        if self.room_manager.exists(room_name):
            await self.send_msg(
                ws,
                CreateRoomMsg(
                    room_name=room_name,
                    state=False
                )
            )
            return

        self.room_manager.create(room_name, data["author_name"])

        await self.send_msg(
            ws,
            CreateRoomMsg(
                room_name=room_name,
                state=True
            )
        )
    
    
    async def handle_enter_room(self, ws, data):
        room_name = data["room_name"]

        if not self.room_manager.exists(room_name):
            await self.send_msg(ws, {
                "type": "enter_room",
                "room_name": room_name,
                "state": False
            })
            return
        
        user_name: str = self.session_manager.get_user_by_socket(ws)

        if user_name is None:
            return

        old_room = self.session_manager.get_room_by_user(user_name)
        
        if old_room is not None:
            self.room_manager.leave(old_room, user_name)
        
        self.session_manager.join_room(user_name, room_name)
        self.room_manager.join(room_name, user_name)
        
        await self.send_msg(ws, {
            "type": "enter_room",
            "room_name": room_name,
            "state": True
        })
    
    
    async def handle_request_chat_messages(self, ws, data):
        room_name = self.session_manager.get_room_by_socket(ws)

        if room_name is None: return

        await self.send_msg(
            ws,
            ChatsMsg(
                messages=self.room_manager.messages(room_name)
            )
        )
    
    
    async def handle_chat_message(self, ws, data):
        user_name: str = self.session_manager.get_user_by_socket(ws)
        
        if user_name is None:
            return
        
        room_name: str = self.session_manager.get_room_by_user(user_name)

        if room_name is None:
            return

        msg: TextMessage = TextMessage(
            id=data["message_id"],
            author=user,
            message=data["message"],
            time=data["time"]
        )

        self.room_manager.add_message(room_name, msg)

        payload = ChatMsg(msg)

        for client_name in self.room_manager.clients(room_name):
            client_ws = self.session_manager.get_socket_by_user(client_name)

            if client_ws is None: continue

            await self.send_msg(client_ws, payload)