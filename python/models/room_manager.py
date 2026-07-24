from models.models import Room, TextMessage

# cd /storage/emulated/0/Programs/Python\ Projects/room
type Rooms = dict[str, Room]


class RoomManager:
    def __init__(self, rooms: Rooms | None = None) -> None:
        self._rooms: Rooms = rooms or {}
    
    
    def _require(self, room_name: str) -> Room:
        room: Room = self._rooms.get(room_name)
    
        if room is None:
            raise ValueError(f'Room "{room_name}" not found')
    
        return room
    
    
    def to_dict(self) -> list:
        return [
            room.to_dict()
            for room in self.rooms()
        ]
    
    
    def create(
        self,
        name: str,
        author: str,
        permanent: bool = False,
        password: str | None = None
    ) -> None:
        if name in self._rooms:
            raise ValueError(f'Room "{name}" already exists')
        
        room: Room = Room(name, author, permanent, password)
        self._rooms[name] = room
        return room
    
    
    def add(self, room: Room) -> None:
        if room.name in self._rooms:
            raise ValueError(f'Room "{room.name}" already exists')
    
        self._rooms[room.name] = room
    
    
    def remove(self, name: str) -> Room:
        return self._rooms.pop(name)
    
    
    def get(self, name: str) -> Room:
        return self._rooms.get(name, None)
    
    
    def clear(self) -> None:
        self._rooms = {}
    
    
    def count(self) -> int:
        return len(self._rooms)
    
    
    def exists(self, name: str) -> bool:
        return name in self._rooms
    
    
    def names(self) -> list[str]:
        return list(self._rooms.keys())
    
    
    def rooms(self) -> list[Room]:
        return list(self._rooms.values())
    
    
    def join(self, room_name: str, user: str) -> None:
        self._require(room_name).add_client(user)
    
    
    def leave(self, room_name: str, user: str) -> None:
        room = self.get(room_name)
    
        if room is None: return
    
        room.remove_client(user)
    
    
    def clients(self, room_name: str) -> set[str]:
        return set(self._require(room_name).clients)
    
    
    def has_client(self, room_name: str, user: str) -> bool:
        return self._rooms[room_name].has_client(user)
    
    
    def add_message(self, room_name: str, msg: TextMessage) -> None:
        self._require(room_name).chat.append(msg)
    
    
    def messages(self, room_name: str) -> list[TextMessage]:
        return self._require(room_name).chat
    
    
    def remove_if_empty(self, room_name: str) -> bool:
        room: Room = self.get(room_name)
    
        if room is None: return False
        if room.permanent: return False
        if not room.empty: return False
    
        del self._rooms[room_name]
        return True