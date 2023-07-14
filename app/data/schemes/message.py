from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str


class Message(MessageBase):
    id: int
    chat_id: int
    owner_id: int
