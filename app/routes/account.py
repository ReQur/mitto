from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from app.data.schemes.token import Token
from app.data.schemes.user import UserCredentials, UserInfo
from app.routes.dependences.authorization import (
    authenticate_user,
    create_access_token,
    AuthException,
    InactiveUserException,
    get_current_active_user,
    create_refresh_token,
    validate_refresh_token,
)

router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


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


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    try:
        user = authenticate_user(
            UserCredentials(
                email=form_data.username, password=form_data.password
            )
        )
    except InactiveUserException:
        raise Unauthorized("Your account was deactivated")
    except AuthException:
        raise Unauthorized("Incorrect username or password")

    access_token = create_access_token(data={"sub": user.__dict__})
    refresh_token = create_refresh_token(data={"sub": user.__dict__})
    response.set_cookie(
        key="X-Refresh-Token", value=refresh_token, httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInfo)
async def read_users_me(
    current_user: Annotated[UserInfo, Depends(get_current_active_user)]
):
    return current_user


@router.get("/refresh", response_model=Token)
async def refresh_tokens(
    current_user: Annotated[UserInfo, Depends(validate_refresh_token)],
    response: Response,
):
    access_token = create_access_token(data={"sub": current_user.__dict__})
    refresh_token = create_refresh_token(data={"sub": current_user.__dict__})
    response.set_cookie(
        key="X-Refresh-Token", value=refresh_token, httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}
