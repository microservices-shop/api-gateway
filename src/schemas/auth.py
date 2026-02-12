from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TokenPayloadSchema(BaseModel):
    """Схема payload JWT токена."""

    sub: UUID = Field(..., description="User ID (subject)")
    email: EmailStr = Field(..., description="User email")
    role: str = Field(..., description="User role (user/admin)")
    type: str = Field(..., description="Token type (access/refresh)")
    iat: datetime = Field(..., description="Issued at")
    exp: datetime = Field(..., description="Expiration time")

    model_config = ConfigDict(from_attributes=True)

    def to_headers(self) -> dict[str, str]:
        return {
            "X-User-ID": str(self.sub),
            "X-User-Email": self.email,
            "X-User-Role": self.role,
        }
