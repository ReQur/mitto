from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.data.schemes.token import Token
from app.data.schemes.user import UserCredentials, UserInfo
from app.routes.dependences.authorization import (
    DeactivatedAccount,
    Unauthorized,
    authorization_handler,
)
from app.services.authorization import AuthException
from app.services.user import (
    user_service,
    InactiveUserException,
    UserServiceException,
)

router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    try:
        user = authorization_handler.authenticate_user(
            UserCredentials(
                email=form_data.username, password=form_data.password
            )
        )
    except (AuthException, UserServiceException, InactiveUserException):
        raise

    access_token = authorization_handler.authorize_user(user, response)
    return access_token


@router.get("/me", response_model=UserInfo)
async def read_users_me(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_access_token)
    ]
):
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    return user


@router.get("/refresh", response_model=Token)
async def refresh_tokens(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_refresh_token)
    ],
    response: Response,
):
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    user = UserInfo(
        email=user.email,
        username=user.username,
        id=user.id,
    )
    access_token = authorization_handler.authorize_user(user, response)
    return access_token
