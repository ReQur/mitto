from typing import Callable
from app.data.database import database


def start() -> Callable:
    async def start_app() -> None:
        await database.connect()

    return start_app


def stop() -> Callable:
    async def stop_app() -> None:
        await database.disconnect()

    return stop_app
