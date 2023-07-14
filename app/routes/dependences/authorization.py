from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.data.crud import get_user_by_email
from app.data.schemes.user import UserCredentials, UserInfo

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
