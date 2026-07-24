import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from models.models import Room, TextMessage


@pytest.fixture
def room():
    return Room(
        name="Python",
        author="Aryel",
        password="1234"
    )


def test_initial_state(room):
    assert room.name == "Python"
    assert room.author == "Aryel"
    assert room.empty
    assert room.clients_count == 0
    assert room.has_password
    assert room.removable is True


def test_add_client(room):
    assert room.add_client("Alice")
    assert room.has_client("Alice")
    assert room.clients_count == 1


def test_add_existing_client(room):
    room.add_client("Alice")

    assert not room.add_client("Alice")
    assert room.clients_count == 1


def test_remove_client(room):
    room.add_client("Alice")

    assert room.remove_client("Alice")
    assert room.empty


def test_remove_nonexistent_client(room):
    assert not room.remove_client("Bob")


def test_has_client(room):
    room.add_client("Alice")

    assert room.has_client("Alice")
    assert not room.has_client("Bob")


def test_password_success(room):
    assert room.check_password("1234")


def test_password_failure(room):
    assert not room.check_password("4321")


def test_has_password(room):
    assert room.has_password


def test_add_message(room):
    msg = TextMessage(
        id="1",
        author="Alice",
        message="Hello",
        time="10:00"
    )

    room.add_message(msg)

    assert room.messages() == [msg]


def test_clear_chat(room):
    room.add_message(
        TextMessage(
            id="1",
            author="Alice",
            message="Hello",
            time="10:00"
        )
    )

    room.clear_chat()

    assert room.messages() == []


def test_messages_returns_copy(room):
    room.add_message(
        TextMessage(
            id="1",
            author="Alice",
            message="Hello",
            time="10:00"
        )
    )

    msgs = room.messages()
    msgs.clear()

    assert len(room.messages()) == 1


def test_room_becomes_not_empty(room):
    room.add_client("Alice")

    assert not room.empty


def test_room_becomes_empty_again(room):
    room.add_client("Alice")
    room.remove_client("Alice")

    assert room.empty


def test_permanent_room_is_not_removable():
    room = Room(
        name="Lobby",
        author="System",
        permanent=True
    )

    assert not room.removable


def test_room_to_dict(room):
    room.add_client("Alice")

    data = room.to_dict()

    assert data["name"] == "Python"
    assert data["author"] == "Aryel"
    assert data["clients_count"] == 1
    assert data["has_password"]