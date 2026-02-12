from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateSchema(BaseModel):
    """Схема для создания продукта (для документации Swagger)."""

    title: str = Field(
        ..., max_length=255, description="Название товара", example="iPhone 15 Pro"
    )
    price: int = Field(..., ge=0, description="Цена в копейках", example=99990)
    category_id: int = Field(..., gt=0, description="ID категории товара", example=1)
    description: str | None = Field(
        None, description="Описание товара", example="Новый смартфон"
    )
    images: list[str] = Field(
        default_factory=list, description="Список URL изображений"
    )
    stock: int = Field(
        default=0, ge=0, description="Количество товара в наличии", example=100
    )
    status: str = Field(
        default="active",
        description="Статус товара (active, archived, draft)",
        example="active",
    )
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Динамические атрибуты товара",
        example={"color": "Титановый", "memory": "256GB"},
    )


class ProductUpdateSchema(BaseModel):
    """Схема для обновления продукта (для документации Swagger)."""

    title: str | None = Field(None, max_length=255, description="Название товара")
    price: int | None = Field(None, ge=0, description="Цена в копейках")
    category_id: int | None = Field(None, gt=0, description="ID категории товара")
    description: str | None = Field(None, description="Описание товара")
    images: list[str] | None = Field(None, description="Список URL изображений")
    stock: int | None = Field(None, ge=0, description="Количество товара в наличии")
    status: str | None = Field(
        None, description="Статус товара (active, archived, draft)"
    )
    attributes: dict[str, Any] | None = Field(
        None, description="Динамические атрибуты товара"
    )


class ProductResponseSchema(BaseModel):
    """Схема ответа с данными продукта."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID товара", example=1)
    title: str = Field(..., description="Название товара", example="iPhone 15 Pro")
    price: int = Field(..., description="Цена в копейках", example=99990)
    category_id: int = Field(..., description="ID категории", example=1)
    description: str | None = Field(None, description="Описание товара")
    images: list[str] = Field(
        default_factory=list, description="Список URL изображений товара"
    )
    stock: int = Field(..., description="Количество товара в наличии", example=100)
    status: str = Field(..., description="Статус товара", example="active")
    attributes: dict[str, Any] = Field(..., description="Динамические атрибуты товара")
    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")


class ProductListResponse(BaseModel):
    """Ответ со списком товаров."""

    items: list[ProductResponseSchema] = Field(..., description="Список товаров")
    total: int = Field(..., description="Общее количество элементов")
    page: int = Field(..., description="Текущая страница")
    page_size: int = Field(..., description="Размер страницы")
    total_pages: int = Field(..., description="Всего страниц")
