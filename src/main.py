from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from src.config import settings
from src.exceptions import (
    GatewayException,
    ServiceUnavailableError,
    GatewayTimeoutError,
)
from src.logger import setup_logging, get_logger
from src.middleware.request_logger import RequestLoggingMiddleware
from src.proxy import proxy_client
from src.routes.products import router as products_router
from src.routes.categories import router as categories_router
from src.routes.auth import router as auth_router
from src.routes.users import router as users_router

logger = get_logger(__name__)

setup_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Startup
    await proxy_client.start()
    logger.info("application_startup_complete")
    yield
    # Shutdown
    await proxy_client.stop()
    logger.info("application_shutdown_complete")


app = FastAPI(
    title="API Gateway",
    description="Единая точка входа для микросервисного интернет-магазина",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}


# --- Exception Handlers ---


@app.exception_handler(ServiceUnavailableError)
async def service_unavailable_handler(request: Request, exc: ServiceUnavailableError):
    request_id = structlog.contextvars.get_contextvars().get("request_id")
    logger.error("service_unavailable", detail=exc.detail)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": exc.detail,
            "request_id": request_id,
        },
        headers={"Retry-After": "30"},
    )


@app.exception_handler(GatewayTimeoutError)
async def gateway_timeout_handler(request: Request, exc: GatewayTimeoutError):
    request_id = structlog.contextvars.get_contextvars().get("request_id")
    logger.error("gateway_timeout", detail=exc.detail)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "detail": exc.detail,
            "request_id": request_id,
        },
    )


@app.exception_handler(GatewayException)
async def gateway_exception_handler(request: Request, exc: GatewayException):
    request_id = structlog.contextvars.get_contextvars().get("request_id")
    logger.error("gateway_error", detail=exc.detail)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.detail,
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception")
    request_id = structlog.contextvars.get_contextvars().get("request_id")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please report this ID to support.",
            "request_id": request_id,
        },
    )
