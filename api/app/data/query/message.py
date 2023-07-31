from app.data.schemes.message import Message
from app.data.database import database

ADD_MESSAGE_QUERY = """INSERT INTO message (chat_id, owner_id, text) 
VALUES (:chat_id, :uid, :text)
RETURNING id;
"""

GET_MESSAGES_QUERY = "SELECT * FROM message WHERE chat_id = :chat_id;"


class MessageQuery:
    def __init__(self, db=database):
        self.db = db

    async def add(
        self,
        uid: int,
        chat_id: int,
        text: str,
    ) -> int:
        message_id = await self.db.execute(
            ADD_MESSAGE_QUERY, {"uid": uid, "chat_id": chat_id, "text": text}
        )
        return message_id

    async def get_all(self, chat_id: int) -> list[Message]:
        result = await self.db.fetch_all(
            GET_MESSAGES_QUERY, {"chat_id": chat_id}
        )
        messages = [Message(**message) for message in result]
        return messages


message_query = MessageQuery()
