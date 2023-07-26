from typing import List

from app.data import models
from app.data.database import database
from app.data.schemes.user import UserPublic, UserDB
from app.data.test_data import test_data

GET_USER_BY_EMAIL_QUERY = "SELECT * FROM users WHERE email=:email"
GET_USER_QUERY = "SELECT * FROM users WHERE id=:uid"
GET_ALL_USERS_QUERY = "SELECT * FROM users"


class UserQuery:
    def __init__(self, db=database):
        self.db = db

    async def get_by_email(self, email: str) -> UserDB:
        result = await self.db.fetch_one(
            GET_USER_BY_EMAIL_QUERY, {"email": email}
        )
        if result:
            return UserDB(**result)
        else:
            raise Exception(f"Not found user with email: {email}")

    async def get(
        self,
        uid: int,
    ) -> UserDB:
        result = await self.db.fetch_one(GET_USER_QUERY, {"uid": uid})
        if result:
            return UserDB(**result)
        else:
            raise Exception(f"Not found user with email: {uid}")

    async def get_all(self) -> List[UserDB]:
        result = await self.db.fetch_one(GET_ALL_USERS_QUERY)
        return [UserDB(**user) for user in result]


user_query = UserQuery()
