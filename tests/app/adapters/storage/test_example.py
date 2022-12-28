from unittest.mock import AsyncMock

from app.adapters.storage.example import ExampleAdapter
from tests.app.adapters.storage.conftest import session_ctx_factory


class TestExampleAdapter:
    """Тесты класса ExampleAdapter."""

    async def test__test(self, session):
        """Тестирование метода test()."""
        adapter = AsyncMock(_session_factory=session_ctx_factory(session))
        await ExampleAdapter.get_test(adapter)

        session.execute.assert_awaited_once()
