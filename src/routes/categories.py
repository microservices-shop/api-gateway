from fastapi import APIRouter, Request

from src.config import settings
from src.proxy import proxy_client

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("")
async def get_categories_list(request: Request):
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
async def get_category(category_id: int, request: Request):
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
