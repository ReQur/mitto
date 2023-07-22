from typing import List

from pydantic import BaseModel

from app.data.schemes.message import Message


class ChatBase(BaseModel):
    pass


class ChatUsers(ChatBase):
    user_ids: List[int]


class Chat(ChatUsers):
    id: int
    messages: List[Message]
