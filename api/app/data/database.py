from databases import Database
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)


class DataBaseConnection(Database):
    def __init__(self, url=DATABASE_URL, **kwargs):
        super().__init__(url, **kwargs)

    async def connect(self) -> None:
        try:
            await super().connect()
        except Exception as e:
            logger.warning("--- DB CONNECTION ERROR ---")
            logger.warning(e)
            logger.warning("--- DB CONNECTION ERROR ---")

    async def disconnect(self) -> None:
        try:
            await super().connect()
        except Exception as e:
            logger.warning("--- DB DISCONNECT ERROR ---")
            logger.warning(e)
            logger.warning("--- DB DISCONNECT ERROR ---")


database = DataBaseConnection()
