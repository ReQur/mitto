from app.core.config import ROOT_URL, POSTGRES_DB
from app.data.database import DataBaseConnection


async def create_database_async():
    conn = DataBaseConnection(ROOT_URL)
    try:
        await conn.connect()
        _db = await conn.fetch_all(
            query="SELECT datname FROM pg_database",
        )
        databases = [db['datname'] for db in _db]
        if POSTGRES_DB not in databases:
            await conn.execute(
                query=f"CREATE DATABASE {POSTGRES_DB}"
            )

    finally:
        await conn.disconnect()
