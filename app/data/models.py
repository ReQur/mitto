from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    id: int
    chat_id: int
    owner_id: int
    text: str


@dataclass
class Chat:
    id: int
    user_ids: List[int]
    messages: List[Message]


@dataclass
class User:
    email: str
    username: str | None
    password: str
    id: int
    is_active: bool
    chats: List[Chat]
