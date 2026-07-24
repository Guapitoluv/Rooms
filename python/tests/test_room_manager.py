import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from models.room_manager import RoomManager
from models.models import Room, TextMessage


@pytest.fixture
def manager():
    return RoomManager()


def test_create_room(manager):
    room = manager.create("Python", "Aryel")

    assert room.name == "Python"
    assert manager.exists("Python")


def test_create_duplicate_room(manager):
    manager.create("Python", "Aryel")

    with pytest.raises(ValueError):
        manager.create("Python", "Outro")


def test_add_room(manager):
    room = Room("Sala", "Aryel")

    manager.add(room)

    assert manager.get("Sala") is room


def test_add_duplicate_room(manager):
    manager.add(Room("Sala", "Aryel"))

    with pytest.raises(ValueError):
        manager.add(Room("Sala", "Outro"))


def test_remove_room(manager):
    manager.create("Sala", "Aryel")

    manager.remove("Sala")

    assert not manager.exists("Sala")


def test_get_room(manager):
    room = manager.create("Sala", "Aryel")

    assert manager.get("Sala") is room


def test_get_nonexistent_room(manager):
    assert manager.get("Inexistente") is None


def test_names(manager):
    manager.create("A", "Aryel")
    manager.create("B", "Aryel")

    assert set(manager.names()) == {"A", "B"}


def test_rooms(manager):
    manager.create("A", "Aryel")
    manager.create("B", "Aryel")

    rooms = manager.rooms()

    assert len(rooms) == 2
    assert all(isinstance(room, Room) for room in rooms)


def test_join(manager):
    manager.create("Sala", "Aryel")

    manager.join("Sala", "Alice")

    assert manager.get("Sala").has_client("Alice")


def test_leave(manager):
    manager.create("Sala", "Aryel")

    manager.join("Sala", "Alice")
    manager.leave("Sala", "Alice")

    assert not manager.get("Sala").has_client("Alice")


def test_add_message(manager):
    manager.create("Sala", "Aryel")

    msg = TextMessage(
        id="1",
        author="Alice",
        message="Olá",
        time="10:00"
    )

    manager.add_message("Sala", msg)

    assert manager.messages("Sala") == [msg]


def test_remove_if_empty(manager):
    manager.create("Sala", "Aryel")

    assert manager.remove_if_empty("Sala")
    assert not manager.exists("Sala")


def test_remove_if_empty_with_clients(manager):
    manager.create("Sala", "Aryel")

    manager.join("Sala", "Alice")

    assert not manager.remove_if_empty("Sala")
    assert manager.exists("Sala")


def test_remove_if_empty_permanent():
    manager = RoomManager()

    manager.create(
        "Lobby",
        "System",
        permanent=True
    )

    assert not manager.remove_if_empty("Lobby")
    assert manager.exists("Lobby")