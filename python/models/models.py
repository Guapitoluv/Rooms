from dataclasses import dataclass, field


@dataclass
class TextMessage:
    id: str
    author: str
    message: str
    time: str


@dataclass
class Room:
    name: str
    author: str
    permanent: bool = False
    password: str | None = None
    
    clients: set = field(default_factory=set)
    chat: list[TextMessage] = field(default_factory=list)
    
    def __str__(self) -> str:
        return self.name
    
    
    def __repr__(self) -> str:
        return (
            f"Room("
            f"name={self.name!r}, "
            f"author={self.author!r}, "
            f"clients={len(self.clients)}"
            f")"
        )
    
    
    @property
    def clients_count(self) -> int:
        return len(self.clients)
    
    
    @property
    def has_password(self) -> bool:
        return self.password is not None
    
    
    @property
    def removable(self) -> bool:
        return (
            not self.permanent and
            self.empty
        )
    
    
    @property
    def empty(self) -> bool:
        return len(self.clients) == 0
    
    
    def add_client(self, user: str) -> bool:
        if user in self.clients:
            return False
    
        self.clients.add(user)
        return True
    
    
    def remove_client(self, user: str) -> bool:
        if user not in self.clients:
            return False
    
        self.clients.remove(user)
        return True
    
    
    def has_client(self, user: str) -> bool:
        return user in self.clients
    
    
    def add_message(self, msg: TextMessage) -> None:
        self.chat.append(msg)
    
    
    def messages(self) -> list[TextMessage]:
        return self.chat.copy()
    
    
    def clear_chat(self) -> None:
        self.chat.clear()
    
    
    def check_password(
        self,
        password: str | None
    ) -> bool:
        return self.password == password
    
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "author": self.author,
            "clients_count": len(self.clients),
            "has_password": self.has_password,
            "permanent": self.permanent
        }