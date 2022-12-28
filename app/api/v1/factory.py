from typing import TYPE_CHECKING

from fastapi import FastAPI

from app.api.v1 import handlers
from app.api.v1.routers import example

if TYPE_CHECKING:
    from app.settings.app import AppSettings

PREFIX = "/api/v1"


def build_app(settings: "AppSettings") -> FastAPI:
    """Собрать приложение FastAPI для текущего роута."""
    api_v1 = FastAPI(
        title=f"{settings.title}",
        version=settings.version,
        docs_url="/",
        redoc_url=None,
    )

    # Добавление обработчиков исключений
    handlers.add_all(api_v1)

    # Добавление роутеров
    api_v1.include_router(example.router)

    return api_v1
