from typing import List

from pydantic import BaseModel

from app.data.schemes.message import Message


class ChatBase(BaseModel):
    pass


class Chat(ChatBase):
    id: int
    user_ids: List[int]
    messages: List[Message]
