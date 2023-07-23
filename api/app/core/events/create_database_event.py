from typing import Callable

from app.data.migrations import create_database_async


def create_database() -> Callable:
    async def start_app() -> None:
        await create_database_async()

    return start_app
