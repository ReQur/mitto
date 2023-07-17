from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str


class MessageSend(MessageBase):
    chat_id: int
    owner_id: int


class Message(MessageBase):
    id: int
