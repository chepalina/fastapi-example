from unittest.mock import AsyncMock

from fastapi import status

from app.container import APP_CONTAINER

API_PATH = "/example"


def test__example(client):
    """Тест метода /example."""
    with APP_CONTAINER.example_adapter.override(AsyncMock()):
        response = client.get(f"{API_PATH}")

    assert response.status_code == status.HTTP_200_OK
    assert not response.json()
