import datetime
import json
import logging
import sys
import traceback
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Message, Record

    from utils.logger.settings import LoggerSettings


def setup_logging(
    env: str, system: str, log_level: str, debug: bool, settings: "LoggerSettings"
) -> None:
    """Настроить логирование.

    Оставляем один логгер root, все лог-сообщения обрабатываются им.

    :param env: имя окружения (dev/test/prod/etc);
    :param system: имя системы (имя приложения/микросервиса);
    :param log_level: уровень логирования;
    :param debug: для запуска сервера в режиме разработки;
    :param settings: конфиг логгера.
    """
    # Перехватить все лог-сообщения root логгером.
    log_level = log_level.upper()

    logging.root.handlers = [_InterceptHandler()]
    logging.root.setLevel(log_level)

    # Удалить обработчики и передать сообщения root логгеру.
    loggers = settings.include | settings.debug if debug else settings.include

    for name in loggers:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
        logging.getLogger(name).setLevel(log_level)

    # Отключить обработчики.
    for name in settings.exclude:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = False

    if not debug:
        logger.configure(
            extra={
                "env": env,
                "system": system,
                "inst": settings.instance,
                "component": settings.component_name,
            }
        )
        logger.remove()
        logger.add(sink=_sink, level=log_level, filter=_LogsFilter(settings.ignored))


class _InterceptHandler(logging.Handler):
    """Обработчик для перехватывания сообщений."""

    def emit(self, record: "logging.LogRecord") -> None:
        # Получить соответствующий уровень Loguru, если он существует.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = logging.getLevelName(record.levelno)

        # Найти вызывающий объект, откуда поступило сообщение.
        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            depth += 1
            if frame.f_back is None:
                break

            frame = frame.f_back

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class _LogsFilter:
    """Фильтрация логов."""

    def __init__(self, ignored_paths: list[str]) -> None:
        self.ignored_paths = ignored_paths

    def __call__(self, log_record: "Record") -> bool:
        """Фильтр."""
        return not any(path in log_record["message"] for path in self.ignored_paths)


def _serialize(log_record: "Record") -> str:
    """Сериализовать информацию из лог-сообщения в json.

    :param log_record: информация из лог-сообщения
    :return: json строка
    """
    subset = {
        "@timestamp": log_record["time"]
        .astimezone(datetime.timezone.utc)
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(timespec="milliseconds"),
        "levelname": log_record["level"].name,
        "name": log_record["name"],
        "message": log_record["message"],
        "env": log_record["extra"]["env"],
        "system": log_record["extra"]["system"],
        "inst": log_record["extra"]["inst"],
        "component": log_record["extra"]["component"],
    }
    if exception := log_record["exception"]:
        subset["message"] = (
            f" {subset['message']} {repr(exception.value)} "
            f"{traceback.format_tb(exception.traceback)}"
        )

    return json.dumps(subset)


def _sink(message: "Message") -> None:
    """Вывести в stdout лог-сообщение.

    :param message: лог-сообщение.
    """
    serialized = _serialize(message.record)
    print(serialized, file=sys.stdout)
