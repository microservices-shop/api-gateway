from fastapi import APIRouter, Request

from src.config import settings
from src.dependencies import AdminUserDep
from src.proxy import proxy_client
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("")
async def get_categories_list(request: Request) -> list[CategoryResponseSchema]:
    """
    Получить список всех категорий.

    Маппинг: GET /api/categories → Product Service: GET /api/v1/categories
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/categories",
        service_name="product-service",
    )


@router.get("/{category_id}")
async def get_category(category_id: int, request: Request) -> CategoryResponseSchema:
    """
    Получить категорию по ID.

    Маппинг: GET /api/categories/{category_id} → Product Service: GET /api/v1/categories/{category_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/categories/{category_id}",
        service_name="product-service",
    )


@router.get("/{category_id}/attributes")
async def get_category_attributes(category_id: int, request: Request):
    """
    Получить атрибуты категории.

    Маппинг: GET /api/categories/{category_id}/attributes → Product Service: GET /api/v1/categories/{category_id}/attributes
    """
    # TODO: нужен ли?
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/categories/{category_id}/attributes",
        service_name="product-service",
    )


@router.post("", status_code=201)
async def create_category(
    request: Request,
    user: AdminUserDep,
    body: CategoryCreateSchema,
) -> CategoryResponseSchema:
    """
    Создать новую категорию (доступно только администраторам).

    Маппинг: POST /api/categories → Product Service: POST /api/v1/categories
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/categories",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.patch("/{category_id}")
async def update_category(
    category_id: int,
    request: Request,
    user: AdminUserDep,
    body: CategoryUpdateSchema,
) -> CategoryResponseSchema:
    """
    Обновить категорию (доступно только администраторам).

    Маппинг: PATCH /api/categories/{category_id} → Product Service: PATCH /api/v1/categories/{category_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/categories/{category_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    request: Request,
    user: AdminUserDep,
):
    """
    Удалить категорию (доступно только администраторам).

    Маппинг: DELETE /api/categories/{category_id} → Product Service: DELETE /api/v1/categories/{category_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/categories/{category_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )
