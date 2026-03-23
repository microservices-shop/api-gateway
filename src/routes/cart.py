import uuid

from fastapi import APIRouter, Request, status

from src.config import settings
from src.dependencies import CurrentUserDep
from src.proxy import proxy_client
from src.schemas.cart import (
    AddToCartSchema,
    UpdateQuantitySchema,
    CartItemResponseSchema,
    CartResponseSchema,
    ItemSelectionSchema,
    SelectAllSchema,
)

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("", response_model=CartResponseSchema, status_code=status.HTTP_200_OK)
async def get_cart(
    request: Request,
    user: CurrentUserDep,
) -> CartResponseSchema:
    """
    Получить корзину текущего пользователя.

    Маппинг: GET /api/cart → Cart Service: GET /api/v1/cart
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path="api/v1/cart",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.post(
    "/items", response_model=CartItemResponseSchema, status_code=status.HTTP_201_CREATED
)
async def add_cart_item(
    request: Request,
    user: CurrentUserDep,
    body: AddToCartSchema,
) -> CartItemResponseSchema:
    """
    Добавить товар в корзину.

    Маппинг: POST /api/cart/items → Cart Service: POST /api/v1/cart/items
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path="api/v1/cart/items",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.patch(
    "/items/{item_id}",
    response_model=CartItemResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_cart_item(
    item_id: uuid.UUID,
    request: Request,
    user: CurrentUserDep,
    body: UpdateQuantitySchema,
) -> CartItemResponseSchema:
    """
    Обновить количество товара в корзине.

    Маппинг: PATCH /api/cart/items/{item_id} → Cart Service: PATCH /api/v1/cart/items/{item_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path=f"api/v1/cart/items/{item_id}",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    item_id: uuid.UUID,
    request: Request,
    user: CurrentUserDep,
):
    """
    Удалить товар из корзины.

    Маппинг: DELETE /api/cart/items/{item_id} → Cart Service: DELETE /api/v1/cart/items/{item_id}
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path=f"api/v1/cart/items/{item_id}",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    request: Request,
    user: CurrentUserDep,
):
    """
    Очистить корзину.

    Маппинг: DELETE /api/cart → Cart Service: DELETE /api/v1/cart
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path="api/v1/cart",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.patch(
    "/items/{item_id}/select",
    response_model=CartItemResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def change_item_selection(
    item_id: uuid.UUID,
    request: Request,
    user: CurrentUserDep,
    body: ItemSelectionSchema,
) -> CartItemResponseSchema:
    """
    Переключить статус выбора товара в корзине.

    Маппинг: PATCH /api/cart/items/{item_id}/select → Cart Service: PATCH /api/v1/cart/items/{item_id}/select
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path=f"api/v1/cart/items/{item_id}/select",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )


@router.patch(
    "/select-all", response_model=CartResponseSchema, status_code=status.HTTP_200_OK
)
async def select_all(
    request: Request,
    user: CurrentUserDep,
    body: SelectAllSchema,
) -> CartResponseSchema:
    """
    Выбрать или снять выбор со всех доступных товаров в корзине.

    Маппинг: PATCH /api/cart/select-all → Cart Service: PATCH /api/v1/cart/select-all
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.CART_SERVICE_URL,
        path="api/v1/cart/select-all",
        service_name="cart-service",
        extra_headers=user.to_headers(),
    )
