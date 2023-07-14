from app.data import models
from app.data.test_data import test_data


def get_user_by_email(email: str, db: dict = test_data) -> models.User:
    for user in db['users'].values():
        if user.email == email:
            return user
    raise Exception(f"Not found user with email: {email}")


def get_user(uid: int, db: dict = test_data) -> models.User:
    for user in db['users'].values():
        if user.id == uid:
            return user
    raise Exception(f"Not found user with email: {uid}")
