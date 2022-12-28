"""Модуль для работы с Alembic.

Обеспечивает подключение настроек alembic, подключение к БД из конфигов.
"""

import asyncio
from logging.config import fileConfig

from alembic import context as environment_context
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy.future.engine import Connection

from app.container import APP_CONTAINER
from app.models import *  # импортируются все модели, чтобы для всех моделей создавались миграции

# получение настроек из alembic.ini
context: EnvironmentContext = environment_context  # type: ignore
config: Config = context.config

# Настройка логов из alembic.ini
fileConfig(config.config_file_name)  # type: ignore

target_metadata = BaseModel.metadata


def do_run_migrations(connection: Connection) -> None:
    """Выполнить миграции."""
    db_settings = APP_CONTAINER.db_settings()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    connection.dialect.default_schema_name = db_settings.app_schema

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.
    """
    async with APP_CONTAINER.engine().begin() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    raise RuntimeError("Unsupported operation. Online mode is available only.")

asyncio.run(run_migrations_online())
