from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.data.schemes.user import UserCredentials, UserInfo
from app.services.authorization import (
    authorization_service,
    AuthException,
    AuthorizationService,
)
from app.services.user import UserServiceException, InactiveUserException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")


class Unauthorized(HTTPException):
    def __init__(
        self,
        message: str,
    ) -> None:
        headers = {"WWW-Authenticate": "Bearer"}
        status_code: int = status.HTTP_401_UNAUTHORIZED
        super().__init__(
            status_code=status_code, detail=message, headers=headers
        )


class DeactivatedAccount(HTTPException):
    def __init__(
        self,
    ) -> None:
        status_code: int = status.HTTP_401_UNAUTHORIZED
        super().__init__(
            status_code=status_code, detail="Your account is deactivated"
        )


class AuthorizationHandler:
    scheme: OAuth2PasswordBearer
    _authorization_service: AuthorizationService

    def __init__(
        self,
        scheme=oauth2_scheme,
        _authorization_service=authorization_service,
    ):
        self.scheme = scheme
        self._authorization_service = _authorization_service

    def authenticate_user(self, credentials: UserCredentials) -> UserInfo:
        try:
            return self._authorization_service.authenticate_user(credentials)
        except InactiveUserException:
            raise DeactivatedAccount()
        except (AuthException, UserServiceException):
            raise Unauthorized("Invalid credentials")

    async def validate_refresh_token(
        self,
        request: Request,
    ) -> UserInfo:
        refresh_token = request.cookies.get("X-Refresh-Token")
        return await self.validate_token(refresh_token)

    async def validate_access_token(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UserInfo:
        return await self.validate_token(token)

    async def validate_token(self, token: str):
        try:
            return await self._authorization_service.validate_token(token)
        except AuthException:
            raise Unauthorized(
                "Your token got invalid. Please reauthenticate to the system"
            )


authorization_handler = AuthorizationHandler()
