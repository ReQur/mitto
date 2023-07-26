from typing import List

from pydantic import BaseModel

from app.data.schemes.message import Message


class ChatBase(BaseModel):
    pass


class ChatUsers(ChatBase):
    user_ids: List[int]


class ChatDB(BaseModel):
    id: int
    is_active: bool


class ChatWithMessages(ChatDB):
    messages: List[Message]
