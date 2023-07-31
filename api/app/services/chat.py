from app.data.query.chat import ChatQuery, chat_query
from app.data.schemes.chat import ChatUsers, ChatDB


class ChatServiceException(Exception):
    pass


class ChatService:
    query: ChatQuery

    def __init__(self, query=chat_query):
        self.query = query

    async def add(self, users: ChatUsers) -> int:
        return (await self.query.add(users.user_ids)).id

    async def get_all(self, uid: int) -> list[ChatDB]:
        return await self.query.get_all(uid)

    async def get(self, uid: int, chat_id) -> ChatDB:
        return await self.query.get(uid, chat_id)


chat_service = ChatService()
