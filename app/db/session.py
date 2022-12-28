from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def get_context(session_maker: "sessionmaker") -> AsyncIterator["AsyncSession"]:
    """Контекстный менеджер для создания сессии."""
    async with session_maker.begin() as session:
        yield session
