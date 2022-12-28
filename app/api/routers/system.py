from http import HTTPStatus

from fastapi import APIRouter, Response

from app.api.routers.schemas import VersionSchema
from app.container import APP_CONTAINER

SYSTEM_TAG = "system"
SYSTEM_PREFIX = f"/{SYSTEM_TAG}"

router = APIRouter(prefix=SYSTEM_PREFIX, tags=[SYSTEM_TAG])


@router.get(
    "/liveness",
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
    responses={
        HTTPStatus.NO_CONTENT.value: {"description": HTTPStatus.NO_CONTENT.phrase},
    },
)
async def liveness() -> None:
    """Проверка доступности сервиса."""
    return None


@router.get(
    "/readiness",
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
    responses={
        HTTPStatus.NO_CONTENT.value: {"description": HTTPStatus.NO_CONTENT.phrase},
        HTTPStatus.SERVICE_UNAVAILABLE.value: {
            "description": HTTPStatus.SERVICE_UNAVAILABLE.phrase
        },
    },
)
async def readiness() -> None:
    """Проверка готовности сервиса."""
    return None


@router.get(
    "/version",
    status_code=HTTPStatus.OK,
    response_model=VersionSchema,
)
async def version() -> VersionSchema:
    """Получить текущую версию приложения."""
    return VersionSchema(version=APP_CONTAINER.app_settings().version)
