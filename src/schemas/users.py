from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserResponseSchema(BaseModel):
    """Схема ответа с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Адрес электронной почты пользователя")
    name: str = Field(..., description="Отображаемое имя пользователя")
    picture_url: str | None = Field(
        None, description="URL фотографии профиля пользователя"
    )
    role: str = Field(..., description="Роль пользователя (user, admin)")
    is_active: bool = Field(..., description="Активен ли аккаунт пользователя")
    created_at: datetime = Field(...)


class UserUpdateSchema(BaseModel):
    """Схема для обновления профиля пользователя."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Новое отображаемое имя",
        examples=["Александр"],
    )
    picture_url: str | None = Field(
        None,
        description="Новый URL аватара пользователя",
    )
