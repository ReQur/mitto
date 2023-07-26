from typing import List

from pydantic import BaseModel

from app.data.schemes.chat import Chat


class UserBase(BaseModel):
    email: str
    username: str | None = None


class UserCredentials(UserBase):
    password: str


class UserInfo(UserBase):
    id: int


class UserPublic(UserInfo):
    is_active: bool


class UserDB(UserPublic, UserCredentials):
    pass


class User(UserInfo):
    is_active: bool
    chats: List[Chat]
