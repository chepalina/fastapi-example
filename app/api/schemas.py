from pydantic import BaseModel


class ResponseErrorSchema(BaseModel):
    """Схема ответов с ошибкой."""

    message: str
