from app.data import models
from app.data.query.user import UserQuery, user_query


class UserServiceException(Exception):
    pass


class InactiveUserException(UserServiceException):
    pass


class UserService:
    query: UserQuery

    def __init__(self, query=user_query):
        self.query = query

    def _get(
        self, uid: int = None, email: str = None
    ) -> models.User | dict[str, models.User]:
        if uid:
            return self.query.get(uid)
        elif email:
            return self.query.get_by_email(email)
        else:
            return self.query.get_all()

    def get(
        self, uid: int = None, email: str = None, verify_active=True
    ) -> models.User:
        try:
            user = self._get(uid, email)
        except Exception:
            raise UserServiceException("User not found")

        if verify_active:
            if not user.is_active:
                raise InactiveUserException()

        return user


user_service = UserService()
