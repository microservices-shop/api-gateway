from fastapi import APIRouter, Request

from src.config import settings
from src.dependencies import CurrentUserDep
from src.proxy import proxy_client
from src.schemas.users import UserResponseSchema, UserUpdateSchema

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_profile(
    request: Request,
    user: CurrentUserDep,
) -> UserResponseSchema:
    """
    Получить профиль текущего пользователя.

    Маппинг: GET /api/users/me → Auth Service: GET /api/v1/users/me
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/users/me",
        service_name="auth-service",
        extra_headers=user.to_headers(),
    )


@router.patch("/me", response_model=UserResponseSchema)
async def update_current_user_profile(
    request: Request,
    user: CurrentUserDep,
    body: UserUpdateSchema,
) -> UserResponseSchema:
    """
    Обновить профиль текущего пользователя.

    Маппинг: PATCH /api/users/me → Auth Service: PATCH /api/v1/users/me
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.AUTH_SERVICE_URL,
        path="api/v1/users/me",
        service_name="auth-service",
        extra_headers=user.to_headers(),
    )
