from fastapi import APIRouter, Request

from src.config import settings
from src.dependencies import AdminUserDep
from src.proxy import proxy_client
from src.schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductListResponse,
    ProductResponseSchema,
)

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("")
async def get_products_list(request: Request) -> ProductListResponse:
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
async def get_product_by_id(product_id: int, request: Request) -> ProductResponseSchema:
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


@router.post("")
async def create_product(
    request: Request,
    user: AdminUserDep,
    body: ProductCreateSchema,
) -> ProductResponseSchema:
    """
    Создать новый товар (доступно только администраторам).

    Маппинг: POST /api/products → Product Service: POST /api/v1/products
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/products",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    request: Request,
    user: AdminUserDep,
    body: ProductUpdateSchema,
) -> ProductResponseSchema:
    """
    Обновить товар (доступно только администраторам).

    Маппинг: PATCH /api/products/{product_id} → Product Service: PATCH /api/v1/products/{product_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/products/{product_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    request: Request,
    user: AdminUserDep,
):
    """
    Удалить товар (доступно только администраторам).

    Маппинг: DELETE /api/products/{product_id} → Product Service: DELETE /api/v1/products/{product_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/products/{product_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )
