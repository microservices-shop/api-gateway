from fastapi import APIRouter, Request, status

from src.config import settings
from src.dependencies import AdminUserDep
from src.proxy import proxy_client
from src.schemas.attributes import (
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributeResponseSchema,
)

router = APIRouter(prefix="/api/attributes", tags=["Attributes"])


@router.get("", response_model=list[AttributeResponseSchema])
async def get_attributes(request: Request) -> list[AttributeResponseSchema]:
    """
    Получить список атрибутов (опционально фильтр по category_id).

    Маппинг: GET /api/attributes → Product Service: GET /api/v1/attributes
    Query: category_id (int | None)
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/attributes",
        service_name="product-service",
    )


@router.get("/{attribute_id}", response_model=AttributeResponseSchema)
async def get_attribute(attribute_id: int, request: Request) -> AttributeResponseSchema:
    """
    Получить атрибут по ID.

    Маппинг: GET /api/attributes/{attribute_id} → Product Service: GET /api/v1/attributes/{attribute_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/attributes/{attribute_id}",
        service_name="product-service",
    )


@router.post(
    "", response_model=AttributeResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_attribute(
    request: Request,
    user: AdminUserDep,
    body: AttributeCreateSchema,
) -> AttributeResponseSchema:
    """
    Создать атрибут (только для администраторов).

    Маппинг: POST /api/attributes → Product Service: POST /api/v1/attributes
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path="api/v1/attributes",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.patch("/{attribute_id}", response_model=AttributeResponseSchema)
async def update_attribute(
    attribute_id: int,
    request: Request,
    user: AdminUserDep,
    body: AttributeUpdateSchema,
) -> AttributeResponseSchema:
    """
    Обновить атрибут (только для администраторов).

    Маппинг: PATCH /api/attributes/{attribute_id} → Product Service: PATCH /api/v1/attributes/{attribute_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/attributes/{attribute_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )


@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(
    attribute_id: int,
    request: Request,
    user: AdminUserDep,
):
    """
    Удалить атрибут (только для администраторов).

    Маппинг: DELETE /api/attributes/{attribute_id} → Product Service: DELETE /api/v1/attributes/{attribute_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.PRODUCT_SERVICE_URL,
        path=f"api/v1/attributes/{attribute_id}",
        service_name="product-service",
        extra_headers=user.to_headers(),
    )
