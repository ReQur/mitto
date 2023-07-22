from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.data.query.token import TokenQuery
from app.data.schemes.user import UserCredentials, UserInfo
from app.services.user import UserService, user_service

DEFAULT = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

QUERY = TokenQuery()


class AuthException(Exception):
    pass


class AuthorizationService:
    # Injections
    query: TokenQuery
    users: UserService

    # Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_WEEKS: int

    def __init__(
        self,
        _query: TokenQuery = QUERY,
        secret: str = DEFAULT,
        algorithm: str = "HS256",
        access_token_expires_minutes: int = 30,
        refresh_token_expires_weeks: int = 4,
        _user_service: UserService = user_service,
    ):
        self.query = _query
        self.users = _user_service

        self.SECRET_KEY = secret
        self.ALGORITHM = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expires_minutes
        self.REFRESH_TOKEN_EXPIRE_WEEKS = refresh_token_expires_weeks

        self.access_token_timedelta = timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.refresh_token_timedelta = timedelta(
            weeks=self.REFRESH_TOKEN_EXPIRE_WEEKS
        )

    def authenticate_user(self, credentials: UserCredentials) -> UserInfo:
        # TODO: Move user service injection to higher level
        user = self.users.get(email=credentials.email)
        if not user or not user.password == credentials.password:
            raise AuthException("Incorrect login or password")

        return UserInfo(
            email=user.email,
            username=user.username,
            id=user.id,
        )

    def create_access_token(self, sub: dict) -> str:
        return self._create_token(
            sub=sub,
            purpose={"purp": "access"},
            lifetime=self.access_token_timedelta,
        )

    def create_refresh_token(self, sub: dict) -> str:
        token = self._create_token(
            sub=sub,
            purpose={"purp": "refresh"},
            lifetime=self.refresh_token_timedelta,
        )
        self.query.add(token)
        return token

    def _create_token(
        self, sub: dict, purpose: dict, lifetime: timedelta
    ) -> str:
        expire = datetime.utcnow() + lifetime
        to_encode = {"sub": sub.copy(), "exp": expire} | purpose

        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_jwt

    async def validate_token(
        self,
        token: str,
    ) -> UserInfo:
        """
        WARNING: -> UserInfo is not an actual user. It is payload from token
        :param token:
        :return: JWT subject payload
        """
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM],
                options={"verify_sub": False},
            )
        except JWTError:
            raise AuthException("Invalid token")

        if payload.get("purp", "access") == "refresh":
            if not self.query.check(token):
                raise AuthException("Blacklisted refresh token")

            self.query.disable(token)

        subject: UserInfo = UserInfo(**payload.get("sub"))
        if subject is None:
            raise AuthException("An empty value in JWT payload")

        return subject


authorization_service = AuthorizationService()
