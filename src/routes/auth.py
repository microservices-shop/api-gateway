from fastapi import APIRouter, Request, status

from src.config import settings
from src.proxy import proxy_client

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.get("/google", status_code=status.HTTP_302_FOUND)
async def google_login(request: Request):
    """
    Инициализация входа через Google.
    Проксирует запрос в Auth Service: GET /api/v1/auth/google
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/auth/google",
        service_name="auth-service",
    )


@router.get("/google/callback", status_code=status.HTTP_302_FOUND)
async def google_callback(request: Request):
    """
    Обработка колбэка от Google.
    Проксирует запрос в Auth Service: GET /api/v1/auth/google/callback
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/auth/google/callback",
        service_name="auth-service",
    )


@router.post("/refresh")
async def refresh_tokens(request: Request):
    """
    Обновление токенов (refresh token в куках).
    Проксирует запрос в Auth Service: POST /api/v1/auth/refresh
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/auth/refresh",
        service_name="auth-service",
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request):
    """
    Выход из системы (удаление refresh token).
    Проксирует запрос в Auth Service: POST /api/v1/auth/logout
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/auth/logout",
        service_name="auth-service",
    )
