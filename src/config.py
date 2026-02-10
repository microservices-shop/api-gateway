from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    """Загрузка переменных окружения"""

    model_config = SettingsConfigDict(
        env_file=str(env_path), case_sensitive=True, extra="ignore"
    )

    # URL внутренних сервисов (Docker network)
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    PRODUCT_SERVICE_URL: str = "http://product-service:8002"
    CART_SERVICE_URL: str = "http://cart-service:8003"
    ORDER_SERVICE_URL: str = "http://order-service:8004"

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"

    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    PROXY_TIMEOUT_CONNECT: float = 5.0
    PROXY_TIMEOUT_READ: float = 30.0
    PROXY_TIMEOUT_WRITE: float = 10.0
    PROXY_MAX_RETRIES: int = 3


settings = Settings()
