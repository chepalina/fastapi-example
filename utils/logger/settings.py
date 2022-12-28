import socket
from typing import Optional

from utils.settings.json import JsonSettings


class LoggerSettings(JsonSettings):
    """Настройки логгера."""

    # Игнорируемые строки
    ignored: list[str] = []
    # Инстанс приложения
    instance: str = socket.gethostname()
    # Название компоненты
    component_name: Optional[str]

    include: set[str] = {
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
    }

    debug: set[str] = {
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "sqlalchemy.orm",
        "sqlalchemy.dialects",
    }

    exclude: set[str] = set()

    class Config:
        env_prefix = "logger_"

        fields = {"component_name": {"env": "component_name"}}
