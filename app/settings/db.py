from datetime import timedelta

from utils.settings.json import JsonSettings


class DBSettings(JsonSettings):
    """Класс настройки подключения к базе данных."""

    # Схема в url в БД.
    url_schema: str = "postgresql"
    # Синхронный драйвер подключения к БД, например asyncpg
    async_driver: str = "asyncpg"
    # Пользователь БД.
    user: str
    # Пароль БД.
    password: str
    # Хост БД.
    host: str
    # Порт БД.
    port: str
    # Имя БД.
    name: str

    # Схема приложения в БД.
    app_schema: str

    # Начальное количество подключений к БД
    start_pool_size: int = 1
    # Максимальное количество подключений к БД
    max_pool_size: int = 1
    # Время, через которое пересоздается подключение к БД если оно не было использовано
    connection_timeout: timedelta = timedelta(seconds=5)

    # Автоматическая отправка запроса.
    autoflush: bool = False
    # Автоматическая фиксация транзакции.
    autocommit: bool = False
    # Обновлять объект после фиксации транзакции.
    expire_on_commit: bool = False

    @property
    def url(self) -> str:
        """Ссылка для подключения к БД с использованием асинхронного драйвера."""
        schema = f"{self.url_schema}+{self.async_driver}"
        return f"{schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_prefix = "db_"
