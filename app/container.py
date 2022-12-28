from contextlib import AbstractAsyncContextManager
from pathlib import Path
from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Dependency, Provider, Singleton
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.adapters.storage.example import ExampleAdapter
from app.db import engine, session
from app.settings.app import AppEnvSettings, AppSettings
from app.settings.db import DBSettings
from app.settings.server import ServerSettings
from utils.logger.settings import LoggerSettings
from utils.logger.setup import setup_logging
from utils.pyproject import PyProjectData

if TYPE_CHECKING:
    from logging import Logger

    from sqlalchemy.ext.asyncio import AsyncEngine


# Корневая директория проекта
_BASE_DIR = Path(__file__).absolute().parent.parent
_PYPROJECT_FILE = _BASE_DIR / "pyproject.toml"


class AppContainer(DeclarativeContainer):
    """Контейнер зависимостей приложения."""

    _app_env_settings: Singleton["AppEnvSettings"] = Singleton(AppEnvSettings)
    _pyproject: Singleton[PyProjectData] = Singleton(PyProjectData.get_data, _PYPROJECT_FILE)

    app_settings: Singleton["AppSettings"] = Singleton(
        AppSettings, _app_env_settings.provided, _pyproject.provided
    )
    db_settings: Singleton["DBSettings"] = Singleton(DBSettings)
    server_settings: Singleton["ServerSettings"] = Singleton(ServerSettings)
    logger_settings: Singleton["LoggerSettings"] = Singleton(
        LoggerSettings, ignored=app_settings.provided.ignored_paths
    )

    logger: Provider["Logger"] = Dependency()

    setup_logging: Callable[None] = Callable(
        setup_logging,
        env=app_settings.provided.env,
        system=app_settings.provided.tag,
        log_level=server_settings.provided.log_level,
        debug=server_settings.provided.debug,
        settings=logger_settings.provided,
    )

    engine: Singleton["AsyncEngine"] = Singleton(engine.get_async, settings=db_settings.provided)

    session_maker: Singleton["sessionmaker"] = Singleton(
        sessionmaker,
        bind=engine.provided,
        class_=AsyncSession,
        autoflush=db_settings.provided.autoflush,
        autocommit=db_settings.provided.autocommit,
        expire_on_commit=db_settings.provided.expire_on_commit,
    )

    session_ctx: Callable[AbstractAsyncContextManager["AsyncSession"]] = Callable(
        session.get_context, session_maker=session_maker.provided
    )

    example_adapter: Singleton["ExampleAdapter"] = Singleton(ExampleAdapter, session_ctx.provider)


APP_CONTAINER = AppContainer()
