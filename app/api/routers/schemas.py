from pydantic import BaseModel


class VersionSchema(BaseModel):
    """Схема с версией приложения."""

    version: str

    class Config:
        example = schema_extra = {
            "example": {
                "version": "0.1.2",
            }
        }
