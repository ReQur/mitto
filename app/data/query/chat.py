from app.data import models
from app.data.test_data import test_data


class ChatQuery:
    def __init__(self, db=test_data):
        self.db = db

    def add(
        self,
        uids: [int],
    ) -> int:
        chat_id = max(self.db["chats"].keys()) + 1
        self.db["chats"][chat_id] = models.Chat(
            id=chat_id, user_ids=uids, messages=[]
        )
        return chat_id

    def get_all(self, uid: int) -> dict[str, models.Chat]:
        chats: dict[str, models.Chat] = {}
        for chat in self.db["chats"].values():
            if uid in chat.user_ids:
                chats[chat.id] = chat
        return chats


chat_query = ChatQuery()
