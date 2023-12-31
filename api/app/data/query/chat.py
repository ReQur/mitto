from app.data.database import database
from app.data.schemes.chat import ChatDB

ADD_CHAT_QUERY = """WITH new_chat AS (
    INSERT INTO chat (is_active)
    VALUES (true)
    RETURNING id, is_active
),
inserted_users AS (
    INSERT INTO user_chat (user_id, chat_id)
    SELECT user_id, new_chat.id
    FROM new_chat, unnest(:uids ::integer[]) AS user_id
)
SELECT id, is_active FROM new_chat;
"""

GET_ALL_CHATS_QUERY = """SELECT chat.*
FROM chat
JOIN user_chat ON chat.id = user_chat.chat_id 
WHERE user_chat.user_id=:user_id"""

GET_CHAT_QUERY = """SELECT chat.id, chat.is_active
FROM chat
JOIN user_chat ON chat.id = user_chat.chat_id
WHERE user_chat.user_id = :uid AND chat.id = :chat_id;
"""


class ChatQuery:
    def __init__(self, db=database):
        self.db = db

    async def add(
        self,
        uids: [int],
    ) -> ChatDB:
        result = await self.db.fetch_one(ADD_CHAT_QUERY, {"uids": uids})
        return ChatDB(**result)

    async def get_all(self, uid: int) -> list[ChatDB]:
        result = await self.db.fetch_all(GET_ALL_CHATS_QUERY, {"user_id": uid})
        return [ChatDB(**user) for user in result]

    async def get(self, uid: int, chat_id: int) -> ChatDB:
        result = await self.db.fetch_one(
            GET_CHAT_QUERY, {"uid": uid, "chat_id": chat_id}
        )
        return ChatDB(**result)


chat_query = ChatQuery()
