from typing import TYPE_CHECKING, Optional

from utils.settings.json import JsonSettings

if TYPE_CHECKING:
    from utils.pyproject import PyProjectData


class AppEnvSettings(JsonSettings):
    """Настройки информации о приложении из переменных окружения."""

    # Имя среды
    tag: Optional[str] = None
    # Тег среды
    env: str
    # Версия приложения
    version: Optional[str] = None
    # Пути игнорируемые при access логах и метриках.
    ignored_paths: set[str] = {
        "/system/liveness",
        "/system/readiness",
        "/metrics",
    }

    class Config:
        env_prefix = "app_"


class AppSettings:
    """Настройки информации о приложении."""

    def __init__(self, app_settings: AppEnvSettings, py_project_data: "PyProjectData"):
        self.tag = app_settings.tag or py_project_data.get_app_name()
        self.env = app_settings.env
        self.version = app_settings.version or py_project_data.get_app_version()
        self.env_tag = f"{self.tag}_{self.env}"
        self.title = f"{self.tag}_{self.env}".replace("-", "_")
        self.ignored_paths = app_settings.ignored_paths
