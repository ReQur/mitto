from app.data.database import database

ADD_TOKEN_QUERY = "INSERT INTO token (token, is_active) VALUES (:token, true);"
CHEK_TOKEN_QUERY = "SELECT is_active FROM token WHERE token = :token;"
DISABLE_TOKEN_QUERY = (
    "UPDATE token SET is_active = false WHERE token = :token;"
)


class TokenQuery:
    def __init__(self, db=database):
        self.db = db

    async def add(self, token: str) -> None:
        await self.db.execute(ADD_TOKEN_QUERY, {"token": token})

    async def check(self, token: str) -> bool:
        result = await self.db.fetch_one(CHEK_TOKEN_QUERY, {"token": token})
        return result["is_active"] if result else False

    async def disable(self, token: str) -> None:
        await self.db.execute(DISABLE_TOKEN_QUERY, {"token": token})
