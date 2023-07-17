from app.data import models
from app.data.query.chat import ChatQuery, chat_query
from app.data.schemes.chat import ChatUsers, Chat


class ChatServiceException(Exception):
    pass


class ChatService:
    query: ChatQuery

    def __init__(self, query=chat_query):
        self.query = query

    def add(self, users: ChatUsers) -> Chat:
        chat_id = self.query.add(users.user_ids)
        return Chat(id=chat_id, users=users.user_ids, messages=[])

    def get_all(self, uid: int) -> dict[str, models.Chat]:
        return self.query.get_all(uid)

    def get(self, uid: int, chat_id) -> models.Chat:
        return self.query.get(uid, chat_id)


chat_service = ChatService()
