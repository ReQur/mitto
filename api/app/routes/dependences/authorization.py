from typing import Annotated

from fastapi import Depends, Request, HTTPException, status, Response
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
    """Error occurred during authorizing user

    Status Code: status.HTTP_401_UNAUTHORIZED
    Detail: passes from message parameter

    :param message: str - passed to exception details
    :raises HTTPException:
    """

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
    """Trying to get data of deactivated user

    Status Code: status.HTTP_401_UNAUTHORIZED
    Detail: "Your account is deactivated"

    :raises HTTPException:
    """

    def __init__(
        self,
    ) -> None:
        status_code: int = status.HTTP_401_UNAUTHORIZED
        super().__init__(
            status_code=status_code, detail="Your account is deactivated"
        )


class AuthorizationHandler:
    """AuthorizationHandler class for user authentication and authorization.

    Class manages JWT tokens.
    It needs to generate, set and validate these tokens.

    :Attributes:
        scheme: authentication scheme that class uses
        _authorization_service: injected service for authorization

    :Methods:
        init: class initialization
        authenticate_user: authenticate user by credentials
        authorize_user: create access and refresh token pair for user
        validate_refresh_token: validate refresh token from cookie
        validate_access_token: validate access token from header
        validate_token common: method for token validation

    """

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
        """Verify credentials and authorize user

        :param credentials: User credentials from login form
        :return: Info about authorized used from database
        :raise DeactivatedAccount: If requested account is deactivated
        :raise Unauthorized: If credentials are invalid
        """
        try:
            return self._authorization_service.authenticate_user(credentials)
        except InactiveUserException:
            raise DeactivatedAccount()
        except (AuthException, UserServiceException):
            raise Unauthorized("Invalid credentials")

    def authorize_user(
        self, user: UserInfo, response: Response
    ) -> dict[str, str]:
        """
        Creates a pair of access and refresh JW Tokens.
        Set refresh token into a http only cookie
        and return dict with type of Token.
        :param user: UserInfo,
            that data would be turned into a subject of JWT payload
        :param response: FastAPI Response - need to set cookie
        :return: dict[str, str] of type Token
            example {"access_token": access_token, "token_type": "bearer"}
        """
        access_token = self._authorization_service.create_access_token(
            sub=user.__dict__
        )
        refresh_token = self._authorization_service.create_refresh_token(
            sub=user.__dict__
        )
        response.set_cookie(
            key="X-Refresh-Token",
            value=refresh_token,
            httponly=True,
            samesite=None,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def validate_refresh_token(
        self,
        request: Request,
    ) -> UserInfo:
        """Get token from "X-Refresh-Token" http-only cookie
            and pass it to self.validate_token

        :param request: fastAPI.Request
        :return: Claims of type UserInfo from payload of token
        """
        refresh_token = request.cookies.get("X-Refresh-Token")
        return await self.validate_token(refresh_token)

    async def validate_access_token(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UserInfo:
        """Get token from bearer header and pass it to self.validate_token

        :param token: JWT token from oauth2_scheme
        :return: Claims of type UserInfo from payload of token
        """
        return await self.validate_token(token)

    async def validate_token(self, token: str) -> UserInfo:
        """Validate JWT token

        :param token: JWT token generated by this server
        :return: Claims of type UserInfo from payload of token
        """
        try:
            return await self._authorization_service.validate_token(token)
        except AuthException:
            raise Unauthorized(
                "Your token got invalid. Please reauthenticate to the system"
            )


authorization_handler = AuthorizationHandler()
