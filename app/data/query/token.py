class TokenQuery:
    def __init__(self):
        self._db: dict[str, bool] = {}

    def add(self, token: str) -> None:
        self._db[token] = True

    def check(self, token: str) -> bool:
        return self._db.get(token, False)

    def disable(self, token: str) -> None:
        self._db[token] = False
