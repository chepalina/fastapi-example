from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from typing import Any

from pydantic import ValidationError

from utils.base_dir import BASE_DIR
from utils.settings.json import JsonSettings


def validate_settings(*args: str) -> None:
    """Провалидировать настройки.

    :param *args: список путей к настройкам;
    :raises ValueError: ошибки при валидации настроек.
    """
    errors = ""
    for settings_path in args:
        for setting in _get_subclasses(JsonSettings, settings_path):
            try:
                setting()
            except ValidationError as exc:
                errors += f"\n{str(exc)}\n"

    if errors:
        raise ValueError(errors)


def _get_subclasses(parent_class: Any, module_path: str) -> set:
    """Поиск всех подклассов по пути.

    :param parent_class: родительский класс;
    :param module_path: путь до модуля, в котором искать подклассы;
    :return: множество подклассов.
    """
    subclasses = set()
    path = BASE_DIR / Path(*module_path.split("."))

    for _, module_name, _ in iter_modules([str(path)]):

        module = import_module(f"{module_path}.{module_name}")

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and parent_class in attribute.__bases__:
                subclasses.add(attribute)

    return subclasses
