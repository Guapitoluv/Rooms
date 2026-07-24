from websockets.asyncio.server import ServerConnection

class SessionManager:
    def __init__(self) -> None:
        self._user_socket: dict[str, ServerConnection] = {}
        self._socket_user: dict[ServerConnection, str] = {}
        self._user_room: dict[str, str] = {}
    
    
    def identify(self, user_name: str, socket: ServerConnection) -> None:
        old: ServerConnection = self._user_socket.get(user_name)
    
        if old is not None:
            self._socket_user.pop(old, None)
    
        self._user_socket[user_name] = socket
        self._socket_user[socket] = user_name
    
    
    def disconnect(self, socket: ServerConnection) -> tuple[str, str | None] | tuple[None, None]:
        user_name: str = self._socket_user.pop(socket, None)
    
        if user_name is None:
            return None, None
    
        self._user_socket.pop(user_name, None)
        room_name: str = self._user_room.pop(user_name, None)
    
        return user_name, room_name
    
    
    def join_room(self, user_name: str, room_name: str) -> None:
        self._user_room[user_name] = room
    
    
    def leave_room(self, user_name: str) -> str | None:
        return self._user_room.pop(user_name, None)
    
    
    def get_room_by_socket(self, socket: ServerConnection) -> str | None:
        user_name: str = self.get_user(socket)
        
        if user_name is None:
            return None
        
        return self._user_room.get(user_name)
    
    
    def get_room_by_user(self, user_name: str) -> str | None:
        return self._user_room.get(user_name)
    
    
    def get_socket_by_user(self, user_name: str) -> ServerConnection | None:
        return self._user_socket.get(user_name)
    
    
    def get_user_by_socket(self, socket: ServerConnection) -> str | None:
        return self._socket_user.get(socket)