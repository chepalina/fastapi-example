from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import text

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ExampleAdapter:
    """Тестовый Adapter."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_test(self) -> None:
        """Тестовый запрос в базу."""
        async with self._session_factory() as session:
            await session.execute(text("SELECT 1;"))
