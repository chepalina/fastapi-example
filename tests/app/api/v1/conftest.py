from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.factory import build_app

# pylint: disable=redefined-outer-name


@pytest.fixture()
def app_api():
    """Фикстура с приложением FastAPI."""
    app = build_app(MagicMock())

    return app


@pytest.fixture()
def client(app_api):
    """Синхронный тестовый клиент для приложений на FastAPI."""
    with TestClient(app_api) as client:
        yield client
