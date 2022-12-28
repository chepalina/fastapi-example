from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse

from app.api.schemas import ResponseErrorSchema

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def add_all(app: "FastAPI") -> None:
    """Добавить все обработчики ошибок из данного роута к приложению.

    :param app: приложение FastAPI
    """
    app.add_exception_handler(Exception, _unknown_error_handler)


async def _unknown_error_handler(_: "Request", exc: Exception) -> "JSONResponse":
    """Обработчик всех ошибок.

        На случай, если при работе роута возникла ошибка, не обработанная другими хэндлерами.

    :param exc: исключение, обрабатываемое обработчиком
    :return: ответ сервера при получении обрабатываемой ошибки
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseErrorSchema(message=str(exc)).dict(),
    )
