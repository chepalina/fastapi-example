from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import exc as db_exc

from app.api.schemas import ResponseErrorSchema

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def add_all(app: "FastAPI") -> None:
    """Добавить все обработчики ошибок из данного роута к приложению."""
    app.add_exception_handler(db_exc.NoResultFound, _not_found_error_handler)


async def _not_found_error_handler(_request: "Request", exc: Exception) -> "JSONResponse":
    """Обработчик ошибки, при которой ресурс не был найден."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ResponseErrorSchema(message=str(exc)).dict(),
    )
