from app.data import models
from app.data.test_data import test_data


class MessageQuery:
    def __init__(self, db=test_data):
        self.db = db

    def add(
        self,
        uid: int,
        chat_id: int,
        text: str,
    ) -> int:
        message_id = max(self.db["messages"].keys()) + 1
        self.db["messages"][message_id] = models.Message(
            id=message_id, chat_id=chat_id, owner_id=uid, text=text
        )
        return chat_id

    def get_all(self, chat_id: int) -> dict[int, models.Message]:
        messages: dict[int, models.Message] = {}
        for message in self.db["messages"].values():
            if chat_id == message.chat_id:
                messages[message.id] = message
        return messages


message_query = MessageQuery()
