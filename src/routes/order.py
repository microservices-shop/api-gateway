import uuid
from fastapi import APIRouter, Request, status

from src.dependencies import CurrentUserDep
from src.proxy import proxy_client
from src.config import settings

from src.schemas.order import (
    CheckoutResponseSchema,
    PayResponseSchema,
    OrderListResponseSchema,
    OrderDetailResponseSchema,
)

router = APIRouter(prefix="/orders")


@router.post(
    "/checkout",
    response_model=CheckoutResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Оформить заказ",
    description="Создает новый заказ.",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Заказ с таким ключом уже в процессе создания"
        },
        status.HTTP_201_CREATED: {
            "description": "Заказ с таким ключом уже (или только что) был создан",
            "model": CheckoutResponseSchema,
        },
    },
)
async def checkout(
    request: Request,
    user: CurrentUserDep,
) -> CheckoutResponseSchema:
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ORDER_SERVICE_URL,
        path="api/v1/orders/checkout",
        service_name="order-service",
        extra_headers=user.to_headers(),
    )


@router.post(
    "/{order_id}/pay",
    response_model=PayResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Оплатить заказ",
    description="Переводит заказ в статус 'completed' и очищает корзину пользователя.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Заказ не найден"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Некорректный статус заказа для оплаты (отменен или уже оплачен)"
        },
        status.HTTP_409_CONFLICT: {"description": "Заказ еще в процессе создания"},
    },
)
async def pay(
    request: Request,
    order_id: uuid.UUID,
    user: CurrentUserDep,
) -> PayResponseSchema:
    """Оплата заказа и очистка корзины."""
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ORDER_SERVICE_URL,
        path=f"api/v1/orders/{order_id}/pay",
        service_name="order-service",
        extra_headers=user.to_headers(),
    )


@router.get(
    "",
    response_model=list[OrderListResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Список заказов",
    description="Возвращает завершённые заказы пользователя, отсортированные от новых к старым.",
)
async def get_orders(
    request: Request,
    user: CurrentUserDep,
) -> list[OrderListResponseSchema]:
    """Список завершённых заказов для страницы «Мои заказы».

    Если заказов нет - возвращает пустой список.
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ORDER_SERVICE_URL,
        path="api/v1/orders",
        service_name="order-service",
        extra_headers=user.to_headers(),
    )


@router.get(
    "/{order_id}",
    response_model=OrderDetailResponseSchema,
    summary="Детали заказа",
    description="Возвращает детали завершённого заказа с полной информацией о товарах.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Заказ не найден, не принадлежит пользователю или не завершён"
        },
    },
)
async def get_order_details(
    request: Request,
    user: CurrentUserDep,
    order_id: uuid.UUID,
) -> OrderDetailResponseSchema:
    """Детали завершённого заказа.

    Возвращает 404, если заказ не найден, принадлежит другому
    пользователю или ещё не в статусе `completed`.
    """
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ORDER_SERVICE_URL,
        path=f"api/v1/orders/{order_id}",
        service_name="order-service",
        extra_headers=user.to_headers(),
    )
