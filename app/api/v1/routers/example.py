from fastapi import APIRouter

from app.container import APP_CONTAINER

TAG = "example"
PREFIX = f"/{TAG}"

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", summary="Тестовый GET запрос.")
async def example() -> None:
    """Тестовый GET запрос."""
    example_adapter = APP_CONTAINER.example_adapter()

    await example_adapter.get_test()
