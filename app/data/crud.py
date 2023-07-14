from app.data.models import User
from app.data.test_data import test_data


def get_user_by_email(email: str, db: dict = test_data) -> User:
    for user in db['users'].values():
        if user.email == email:
            return user
    raise Exception(f"Not found user with email: {email}")
