from json import loads as json_loads
from typing import TYPE_CHECKING, Any

from pydantic.env_settings import BaseSettings, Extra

from utils.base_dir import BASE_DIR

if TYPE_CHECKING:
    from pydantic.env_settings import SettingsSourceCallable


_JSON_FILE = BASE_DIR / "env.json"
_ENV_FILE_ENCODING = "utf-8"


class JsonSettings(BaseSettings):
    """Базовый класс для чтения настроек из переменных окружения и json-файла.

    Отличается от `pydantic.BaseSettings` тем, что параметр `_env_file` воспринимается ни как
    .env файл, а как JSON.

    JSON файл не должен иметь вложенности. (Значение не может быть словарем).
    """

    class Config(BaseSettings.Config):
        """Статические настройки класса-конфига."""

        env_file_encoding = _ENV_FILE_ENCODING
        extra = Extra.ignore
        case_sensitive = False

        @classmethod
        def customise_sources(
            cls,
            init_settings: "SettingsSourceCallable",
            env_settings: "SettingsSourceCallable",
            file_secret_settings: "SettingsSourceCallable",
        ) -> tuple["SettingsSourceCallable", ...]:
            """Задать порядок источников получения переменных окружения.

            Приоритетность:
            1. аргументы переданные в `__init__`;
            2. переменные окружения;
            3. json-файл с переменными окружения;
            4. папка с секретами.

            :param init_settings: источник настроек переданных в `__init__`;
            :param env_settings: источник настроек из .env и переменных окружения;
            :param file_secret_settings: источник настроек из папки с секретами;
            :return: кортеж источников в порядке приоритета.
            """
            return (
                init_settings,
                _json_settings_source,
                env_settings,
                file_secret_settings,
            )


def _json_settings_source(settings: "BaseSettings") -> dict[str, Any]:
    """Источник настроек, который загружает переменные из JSON файла."""
    if not _JSON_FILE.exists():
        return {}

    encoding = settings.__config__.env_file_encoding
    file_vars = json_loads(_JSON_FILE.read_text(encoding))

    if not settings.__config__.case_sensitive:
        file_vars = {k.lower(): v for k, v in file_vars.items()}

    variables: dict[str, Any] = {}
    for field in settings.__fields__.values():
        field_alias = settings.__config__.env_prefix + field.alias
        field_alias = field_alias if settings.__config__.case_sensitive else field_alias.lower()
        if var := file_vars.get(field_alias):
            variables[field.alias] = var

    return variables
