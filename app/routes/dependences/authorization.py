from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.data.crud import get_user_by_email, get_user
from app.data import models
from app.data.schemes.user import UserCredentials, UserInfo

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")


class AuthException(Exception):
    pass


class InactiveUserException(AuthException):
    pass


def authenticate_user(credentials: UserCredentials) -> UserInfo:
    user = get_user_by_email(credentials.email)
    if not user or not user.password == credentials.password:
        raise AuthException("Incorrect login or password")
    if not user.is_active:
        raise InactiveUserException()

    return UserInfo(
        email=user.email,
        username=user.username,
        id=user.id,
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> models.User:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_sub": False}
        )
        user: UserInfo = UserInfo(**payload.get("sub"))
        if user is None:
            raise AuthException()
    except JWTError:
        raise AuthException()
    _user = get_user(user.id)
    if user is None:
        raise AuthException()
    return _user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> UserInfo:
    if not current_user.is_active:
        raise InactiveUserException()
    return UserInfo(
        email=current_user.email,
        username=current_user.username,
        id=current_user.id,
    )
