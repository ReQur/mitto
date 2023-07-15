from app.data import models
from app.data.test_data import test_data


def get_user_by_email(email: str, db: dict = test_data) -> models.User:
    for user in db["users"].values():
        if user.email == email:
            return user
    raise Exception(f"Not found user with email: {email}")


def get_user(uid: int, db: dict = test_data) -> models.User:
    for user in db["users"].values():
        if user.id == uid:
            return user
    raise Exception(f"Not found user with email: {uid}")


REFRESH_TOKENS: dict[str, bool] = {}


def add_refresh_token(token: str) -> None:
    REFRESH_TOKENS[token] = True


def check_refresh_token(token: str) -> bool:
    return REFRESH_TOKENS[token]


def disable_refresh_token(token: str) -> None:
    REFRESH_TOKENS[token] = False
