from app.data import models
from app.data.test_data import test_data


class UserQuery:
    def __init__(self, db=test_data):
        self.db = db

    def get_by_email(self, email: str) -> models.User:
        for user in self.db["users"].values():
            if user.email == email:
                return user
        raise Exception(f"Not found user with email: {email}")

    def get(
        self,
        uid: int,
    ) -> models.User:
        for user in self.db["users"].values():
            if user.id == uid:
                return user
        raise Exception(f"Not found user with email: {uid}")

    def get_all(self) -> dict[str, models.User]:
        return self.db["users"]


user_query = UserQuery()
