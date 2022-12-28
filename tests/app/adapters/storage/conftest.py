from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture()
def session():
    """Фикстура асинхронной сессии."""
    return AsyncMock(AsyncSession)


def session_ctx_factory(mock):
    """Фабрика async контекстный менеджер, который возвращает переданный объект."""

    @asynccontextmanager
    async def _():
        yield mock

    return _
