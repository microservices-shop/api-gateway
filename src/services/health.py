import asyncio
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

import httpx
from fastapi import Depends

from src.config import settings
from src.logger import get_logger
from src.proxy import proxy_client

logger = get_logger(__name__)


@dataclass
class ServiceHealth:
    """Состояние (доступность) отдельного сервиса."""

    name: str
    url: str
    healthy: bool
    response_time_ms: float
    error: str | None = None


class HealthService:
    """Сервис для проверки доступности внутренних микросервисов."""

    def __init__(self, http_client: httpx.AsyncClient):
        """
        Инициализация сервиса проверки доступности с общим HTTP-клиентом.

        Args:
            http_client: Экземпляр httpx.AsyncClient из proxy_client.
        """
        self.client = http_client
        self.services = {
            "auth-service": settings.AUTH_SERVICE_URL,
            "product-service": settings.PRODUCT_SERVICE_URL,
            "cart-service": settings.CART_SERVICE_URL,
            "order-service": settings.ORDER_SERVICE_URL,
        }

    async def check_service(self, name: str, base_url: str) -> ServiceHealth:
        """
        Проверка доступности одного сервиса.

        Args:
            name: Название сервиса для логирования.
            base_url: Базовый URL сервиса.

        Returns:
            ServiceHealth: Состояние сервиса с временем ответа и деталями ошибки.
        """
        url = f"{base_url}/health"
        start_time = time.perf_counter()

        try:
            response = await self.client.get(url, timeout=settings.HEALTH_CHECK_TIMEOUT)
            response.raise_for_status()
            duration = (time.perf_counter() - start_time) * 1000

            return ServiceHealth(
                name=name,
                url=url,
                healthy=True,
                response_time_ms=round(duration, 2),
            )

        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            error_msg = f"{type(e).__name__}: {str(e)}"

            logger.warning(
                "service_health_check_failed",
                service=name,
                url=url,
                error=error_msg,
                duration_ms=round(duration, 2),
            )

            return ServiceHealth(
                name=name,
                url=url,
                healthy=False,
                response_time_ms=round(duration, 2),
                error=error_msg,
            )

    async def check_all_services(self) -> list[ServiceHealth]:
        """
        Параллельная проверка всех настроенных сервисов.

        Returns:
            Список объектов ServiceHealth со статусом для каждого сервиса.
        """
        tasks = [self.check_service(name, url) for name, url in self.services.items()]
        return await asyncio.gather(*tasks)


@lru_cache
def get_health_service() -> HealthService:
    """
    Провайдер зависимости для HealthService.

    Использует lru_cache для возврата одного и того же экземпляра,
    разделяя HTTP-клиент из proxy_client.

    Returns:
        HealthService: Кэшированный экземпляр HealthService.
    """
    if not proxy_client.client:
        raise RuntimeError(
            "ProxyClient not initialized. Ensure app startup event has completed."
        )
    return HealthService(http_client=proxy_client.client)


HealthServiceDep = Annotated[HealthService, Depends(get_health_service)]
