from app.data import models
from app.data.models import Message
from app.data.query.message import MessageQuery, message_query
from app.data.schemes.message import MessageSend


class MessageServiceException(Exception):
    pass


class MessageService:
    query: MessageQuery

    def __init__(self, query=message_query):
        self.query = query

    def add(self, message: MessageSend) -> Message:
        message_id = self.query.add(
            message.owner_id, message.chat_id, message.text
        )
        return Message(
            id=message_id,
            owner_id=message.owner_id,
            chat_id=message.chat_id,
            text=message.text,
        )

    def get_all(self, chat_id: int) -> dict[int, models.Message]:
        return self.query.get_all(chat_id)


message_service = MessageService()
