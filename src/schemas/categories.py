from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateSchema(BaseModel):
    """Схема для создания категории (для документации Swagger)."""

    title: str = Field(
        ..., max_length=100, description="Название категории", example="Смартфоны"
    )


class CategoryUpdateSchema(BaseModel):
    """Схема для обновления категории (для документации Swagger)."""

    title: str | None = Field(None, max_length=100, description="Название категории")


class CategoryResponseSchema(BaseModel):
    """Схема для ответа с данными категории."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID категории", example=1)
    title: str = Field(..., description="Название категории", example="Смартфоны")
