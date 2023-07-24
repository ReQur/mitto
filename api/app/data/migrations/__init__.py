import logging
from pathlib import Path

import alembic.command
from alembic.config import Config

from app.core.config import ROOT_URL, POSTGRES_DB
from app.data.database import DataBaseConnection

logger = logging.getLogger(__name__)


async def create_database_async():
    conn = DataBaseConnection(ROOT_URL)
    try:
        await conn.connect()
        _db = await conn.fetch_all(
            query="SELECT datname FROM pg_database",
        )
        databases = [db["datname"] for db in _db]
        if POSTGRES_DB not in databases:
            await conn.execute(query=f"CREATE DATABASE {POSTGRES_DB}")
            logger.info(f"Created {POSTGRES_DB} database")
        else:
            logger.info(f"Database {POSTGRES_DB} exists")

    finally:
        await conn.disconnect()


def apply_migrations():
    alembic_cfg = Config(Path("./alembic.ini"))
    alembic.command.upgrade(alembic_cfg, "head")
