class GatewayException(Exception):
    detail = "API Gateway internal error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class ServiceUnavailableError(GatewayException):
    """Сервис недоступен после всех попыток retry."""

    detail = "Service unavailable"


class GatewayTimeoutError(GatewayException):
    """Таймаут при обращении к внутреннему сервису."""

    detail = "Gateway timeout"


class AuthenticationError(GatewayException):
    """JWT токен невалиден, истёк или отсутствует."""

    detail = "Authentication failed"


class ForbiddenError(GatewayException):
    """Недостаточно прав для выполнения операции (требуется admin)."""

    detail = "Forbidden"
