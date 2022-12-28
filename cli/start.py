import click
import uvicorn

from app.settings.server import ServerSettings
from utils.settings.validator import validate_settings

SETTINGS_DIRS = ("app.settings",)


@click.group()
def start() -> None:
    """Запустить один из выбранных сервисов."""


@start.command()
def api() -> None:
    """API-сервис."""

    # Валидация всех настроек.
    validate_settings(*SETTINGS_DIRS)

    # Запуск сервера.
    uvicorn.run(**ServerSettings().dict())
