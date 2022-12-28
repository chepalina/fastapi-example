from typing import TYPE_CHECKING

import toml
from pydantic import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class PoetryToolData(BaseModel):
    """Настройки pyproject.tool.poetry."""

    name: str
    version: str
    description: str
    authors: list[str]


class ToolsData(BaseModel):
    """Настройки pyproject.tool."""

    poetry: PoetryToolData


class PyProjectData(BaseModel):
    """Настройки проекта из pyproject.toml."""

    tool: ToolsData

    def get_app_name(self) -> str:
        """Получить название приложения."""
        return self.tool.poetry.name

    def get_app_version(self) -> str:
        """Получить версию приложения."""
        return self.tool.poetry.version

    @classmethod
    def get_data(cls, path: "Path") -> "PyProjectData":
        """Создать объект PyProjectData."""
        return cls(**toml.load(path))
