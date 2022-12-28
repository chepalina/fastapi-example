from typing import TYPE_CHECKING

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

    from app.settings.db import DBSettings


def get_async(settings: "DBSettings") -> "AsyncEngine":
    """Получить асинхронный `engine` для работы с базой данных."""
    engine = create_async_engine(
        url=settings.url,
        pool_size=settings.start_pool_size,
        max_overflow=settings.max_pool_size,
        pool_timeout=settings.connection_timeout.seconds,
    )

    @event.listens_for(engine.sync_engine, "connect", insert=True)
    def set_search_path(dbapi_conn, _conn_record):
        """Установить схему по умолчанию для коннекта."""
        existing_autocommit = dbapi_conn.autocommit
        dbapi_conn.autocommit = True

        cursor = dbapi_conn.cursor()
        cursor.execute(f"SET search_path TO {settings.app_schema}")
        cursor.close()

        dbapi_conn.autocommit = existing_autocommit

    return engine


async def check_connection(engine: "AsyncEngine") -> None:
    """Проверить соединение с БД."""
    async with engine.begin() as connection:
        await connection.execute(text("SELECT 1;"))
