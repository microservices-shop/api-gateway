import asyncio

import httpx
from fastapi import Request, Response

from src.config import settings
from src.exceptions import GatewayTimeoutError, ServiceUnavailableError
from src.logger import get_logger

logger = get_logger(__name__)


class ProxyClient:
    """HTTP-клиент для проксирования запросов к внутренним сервисам."""

    def __init__(self):
        self.client: httpx.AsyncClient | None = None

    async def start(self):
        """Инициализация httpx.AsyncClient с настройками таймаутов и лимитов."""
        timeout = httpx.Timeout(
            connect=settings.PROXY_TIMEOUT_CONNECT,
            read=settings.PROXY_TIMEOUT_READ,
            write=settings.PROXY_TIMEOUT_WRITE,
            pool=5.0,
        )
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)

        self.client = httpx.AsyncClient(timeout=timeout, limits=limits)
        logger.info(
            "proxy_client_initialized",
            timeout_connect=settings.PROXY_TIMEOUT_CONNECT,
            timeout_read=settings.PROXY_TIMEOUT_READ,
            timeout_write=settings.PROXY_TIMEOUT_WRITE,
        )

    async def stop(self):
        """Корректное закрытие httpx.AsyncClient."""
        if self.client:
            await self.client.aclose()
            logger.info("proxy_client_closed")

    async def forward(
        self,
        request: Request,
        target_base_url: str,
        path: str,
        service_name: str,
        extra_headers: dict[str, str] | None = None,
        max_retries: int | None = None,
    ) -> Response:
        """
        Проксирование запроса к внутреннему сервису с retry логикой.

        Args:
            request: Входящий FastAPI запрос
            target_base_url: URL целевого сервиса
            path: Путь к эндпоинту
            service_name: Имя сервиса для логирования
            extra_headers: Дополнительные заголовки (X-User-ID и т.д.)
            max_retries: Максимальное количество повторов при ConnectError

        Returns:
            Response: Ответ от целевого сервиса

        Raises:
            GatewayTimeoutError: При таймауте запроса
            ServiceUnavailableError: Когда все попытки исчерпаны
        """
        if max_retries is None:
            max_retries = settings.PROXY_MAX_RETRIES

        if not self.client:
            raise RuntimeError("ProxyClient не инициализирован. Вызовите start().")

        # Формирование целевого URL
        target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"
        if request.url.query:
            target_url = f"{target_url}?{request.url.query}"

        # Копирование заголовков (исключая host, content-length)
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)

        # Добавление дополнительных заголовков
        if extra_headers:
            headers.update(extra_headers)

        # Чтение body запроса
        body = await request.body()

        # Retry-цикл
        last_error: Exception | None = None

        for attempt in range(max_retries):
            try:
                logger.debug(
                    "proxy_request_attempt",
                    service=service_name,
                    method=request.method,
                    url=target_url,
                    attempt=attempt + 1,
                    max_retries=max_retries,
                )

                response = await self.client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=body,
                )

                # Успешный ответ — логируем и возвращаем
                logger.info(
                    "proxy_request_success",
                    service=service_name,
                    method=request.method,
                    status_code=response.status_code,
                    attempt=attempt + 1,
                )

                # Фильтрация заголовков ответа
                response_headers = dict(response.headers)
                response_headers.pop("content-encoding", None)
                response_headers.pop("transfer-encoding", None)

                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=response_headers,
                )

            except httpx.ConnectError as exc:
                # Ошибка подключения — retry с exponential backoff
                last_error = exc
                backoff_time = 0.5 * (attempt + 1)

                logger.warning(
                    "proxy_connection_failed",
                    service=service_name,
                    method=request.method,
                    url=target_url,
                    attempt=attempt + 1,
                    max_retries=max_retries,
                    backoff_seconds=backoff_time,
                    error=str(exc),
                )

                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_time)
                continue

            except httpx.TimeoutException as exc:
                # Таймаут — не retryable
                logger.error(
                    "proxy_timeout",
                    service=service_name,
                    method=request.method,
                    url=target_url,
                    error=str(exc),
                )
                raise GatewayTimeoutError(
                    f"Timeout while requesting {service_name}"
                ) from exc

            except httpx.HTTPError as exc:
                # Другие HTTP ошибки — не retryable
                logger.error(
                    "proxy_http_error",
                    service=service_name,
                    method=request.method,
                    url=target_url,
                    error=str(exc),
                )
                raise

        # Все попытки исчерпаны
        logger.error(
            "proxy_all_retries_failed",
            service=service_name,
            method=request.method,
            url=target_url,
            max_retries=max_retries,
            last_error=str(last_error) if last_error else "Unknown",
        )
        raise ServiceUnavailableError(
            f"Service {service_name} is unavailable after {max_retries} retries"
        )


proxy_client = ProxyClient()
