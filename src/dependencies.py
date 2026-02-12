from typing import Annotated

import jwt
from fastapi import Depends, status, Security
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings
from src.exceptions import AuthenticationError
from src.schemas.auth import TokenPayloadSchema

ACCESS_TOKEN_TYPE = "access"

security = HTTPBearer(auto_error=False)


def decode_jwt(token: str) -> TokenPayloadSchema:
    """Декодирование и валидация JWT токена."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

    token_data = TokenPayloadSchema(**payload)

    if token_data.type != ACCESS_TOKEN_TYPE:
        raise AuthenticationError("Token is not an access token")

    return token_data


def get_token(
    creds: HTTPAuthorizationCredentials | None = Security(security),
) -> str:
    """Извлечение Bearer токена из заголовка Authorization."""
    if not creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # credentials = токен
    return creds.credentials


def get_current_user(token: str = Depends(get_token)) -> TokenPayloadSchema:
    """Проверка токена и получение данных текущего пользователя."""
    try:
        token_data = decode_jwt(token)
        return token_data
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_admin(
    user: TokenPayloadSchema = Depends(get_current_user),
) -> TokenPayloadSchema:
    """Проверка прав администратора."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


CurrentUserDep = Annotated[TokenPayloadSchema, Depends(get_current_user)]
AdminUserDep = Annotated[TokenPayloadSchema, Depends(get_current_admin)]
