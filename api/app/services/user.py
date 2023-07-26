from typing import List

from app.data import models
from app.data.query.user import UserQuery, user_query
from app.data.schemes.user import UserPublic, UserDB


class UserServiceException(Exception):
    pass


class InactiveUserException(UserServiceException):
    pass


class UserService:
    query: UserQuery

    def __init__(self, query=user_query):
        self.query = query

    async def _get(
        self, uid: int = None, email: str = None
    ) -> UserDB | List[UserDB]:
        if uid:
            return await self.query.get(uid)
        elif email:
            return await self.query.get_by_email(email)
        else:
            return await self.query.get_all()

    async def get(
        self, uid: int = None, email: str = None, verify_active=True
    ) -> UserDB:
        try:
            user = await self._get(uid, email)
        except Exception:
            raise UserServiceException("User not found")

        if verify_active:
            if not user.is_active:
                raise InactiveUserException()

        return user


user_service = UserService()
