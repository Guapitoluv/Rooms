import sqlite3

from models.models import Room, TextMessage


class Database:
    def __init__(self, path: str = "rooms.db") -> None:
        self._conn = sqlite3.connect(path)
        self._cursor = self._conn.cursor()

        self._create_tables()

    def close(self) -> None:
        self._conn.close()

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def _execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._cursor.execute(sql, params)

    def _fetchone(self, sql: str, params: tuple = ()):
        return self._execute(sql, params).fetchone()

    def _fetchall(self, sql: str, params: tuple = ()):
        return self._execute(sql, params).fetchall()

    def _create_tables(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                name TEXT PRIMARY KEY,
                author TEXT NOT NULL,
                permanent INTEGER NOT NULL,
                password TEXT
            )
        """)

        self._execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                room_name TEXT NOT NULL,
                author TEXT NOT NULL,
                message TEXT NOT NULL,
                time TEXT NOT NULL,
                FOREIGN KEY(room_name) REFERENCES rooms(name)
            )
        """)

        self.commit()

    # -----------------------------
    # Rooms
    # -----------------------------

    def add_room(self, room: Room) -> None:
        self._execute(
            """
            INSERT INTO rooms(name, author, permanent, password)
            VALUES (?, ?, ?, ?)
            """,
            (
                room.name,
                room.author,
                int(room.permanent),
                room.password
            )
        )

        self.commit()

    def remove_room(self, room_name: str) -> None:
        self._execute(
            "DELETE FROM rooms WHERE name=?",
            (room_name,)
        )

        self.commit()

    def exists_room(self, room_name: str) -> bool:
        return self._fetchone(
            "SELECT 1 FROM rooms WHERE name=?",
            (room_name,)
        ) is not None

    def rooms(self):
        return self._fetchall(
            """
            SELECT
                name,
                author,
                permanent,
                password
            FROM rooms
            """
        )
    
    # -----------------------------
    # Messages
    # -----------------------------
    
    def add_message(
        self,
        room_name: str,
        message: TextMessage
    ) -> None:
        self._execute(
            """
            INSERT INTO messages
            (id, room_name, author, message, time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                message.id,
                room_name,
                message.author,
                message.message,
                message.time
            )
        )

        self.commit()
    
    
    def messages(
        self,
        room_name: str
    ) -> list[tuple]:
        return self._fetchall(
            """
            SELECT
                id,
                author,
                message,
                time
            FROM messages
            WHERE room_name=?
            ORDER BY time
            """,
            (room_name,)
        )
    
    
    def clear_messages(
        self,
        room_name: str
    ) -> None:
        self._execute(
            "DELETE FROM messages WHERE room_name=?",
            (room_name,)
        )

        self.commit()