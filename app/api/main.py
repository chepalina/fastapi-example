from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger

from app.api import handlers
from app.api.routers.system import router as system_router
from app.api.v1 import factory as v1
from app.container import APP_CONTAINER
from app.db.engine import check_connection
from utils.monitoring import instrumentator


def create_app():
    """Создать приложение FastAPI."""
    APP_CONTAINER.logger.override(logger)
    APP_CONTAINER.check_dependencies()

    # Настройка логирования.
    APP_CONTAINER.setup_logging()

    settings = APP_CONTAINER.app_settings()

    app = FastAPI(
        title=settings.title,
        version=settings.version,
        docs_url="/",
        redoc_url=None,
    )

    @app.on_event("startup")
    async def startup() -> None:
        """Предварительные действия перед запуском приложения."""

        # Проверка соединения с БД.
        await check_connection(APP_CONTAINER.engine())

    # Подключение системного роутера
    app.include_router(system_router)
    handlers.add_all(app)

    # Подключение приложений.
    _mount_app(app, v1.build_app(settings), v1.PREFIX)

    metrics_instrumentator = instrumentator.get_instrumentator(
        settings.title, list(settings.ignored_paths)
    )
    metrics_instrumentator.instrument(app).expose(app)

    return app


def _mount_app(app: "FastAPI", sub_app: "FastAPI", sub_app_prefix: str) -> None:
    """Примонтировать приложение."""
    handlers.add_all(sub_app)
    app.mount(sub_app_prefix, sub_app)
    _fix_route_operation_ids(sub_app)


def _fix_route_operation_ids(app: "FastAPI") -> None:
    """Исправить автогенерируемые operation_id роутов.

    Для корректных и неизбыточных названий методов в автоклиентах в качестве operation_id
    используются имена роутов. Вызывать только после добавления роутов.

    :param app: объект приложения FastAPI;
    :raise RuntimeError: дублирование operation_id.
    """
    unique_operation_ids: set[str] = set()

    for route in app.routes:

        if isinstance(route, APIRoute):

            if (operation_id := route.name) not in unique_operation_ids:
                unique_operation_ids.add(operation_id)
                route.operation_id = operation_id
            else:
                raise RuntimeError(f'Duplicate operation_id "{operation_id}" from route "{route}".')
