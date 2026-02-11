from fastapi import APIRouter, Request

from src.config import settings
from src.proxy import proxy_client

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("")
async def get_products_list(request: Request):
    """
    Получить список всех товаров (публичный эндпоинт).

    Маппинг: GET /api/products → Product Service: GET /api/v1/products
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/products",
        service_name="product-service",
    )


@router.get("/{product_id}")
async def get_product_by_id(product_id: int, request: Request):
    """
    Получить конкретный товар по ID (публичный эндпоинт).

    Маппинг: GET /api/products/{product_id} → Product Service: GET /api/v1/products/{product_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/products/{product_id}",
        service_name="product-service",
    )
