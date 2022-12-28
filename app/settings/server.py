from utils.settings.json import JsonSettings


class ServerSettings(JsonSettings):
    """Настройки uvicorn сервера."""

    # Путь до ASGI в формате "<module>:<attribute>"
    app: str = "app.api.main:create_app"
    # Рассматривать `app` как фабрику
    factory: bool = True
    # Количество воркеров сервера
    workers: int = 1
    # Флаг запуска сервера в режиме разработки
    debug: bool = False
    # Уровень логирования
    log_level: str = "info"
    # Event loop
    loop: str = "auto"
    # Хост приложения
    host: str
    # Порт приложения
    port: int

    class Config:
        env_prefix = "server_"
