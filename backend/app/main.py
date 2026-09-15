from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.middleware.audit import AuditMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.api.v1 import system, web, api_testing, adapters, history, targets

settings = get_settings()
setup_logging(settings.log_level)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting_app", version=settings.app_version)
    await init_db()
    logger.info("database_initialized")
    yield
    from app.services.web_testing import web_service
    from app.services.api_testing import api_service
    from app.adapters.cloudflare_adapter import cloudflare_adapter
    from app.adapters.recaptcha_adapter import recaptcha_adapter

    await web_service.close()
    await api_service.close()
    await cloudflare_adapter.close()
    await recaptcha_adapter.close()
    logger.info("app_shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Zeron Web Security Testing Suite",
        description="Advanced web security testing platform for authorized security testing",
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=settings.rate_limit_per_minute)
    app.add_middleware(AuditMiddleware)

    app.include_router(system.router, prefix="/api/v1", tags=["System"])
    app.include_router(web.router, prefix="/api/v1/web", tags=["Web Testing"])
    app.include_router(api_testing.router, prefix="/api/v1/api", tags=["API Testing"])
    app.include_router(adapters.router, prefix="/api/v1", tags=["Adapters"])
    app.include_router(history.router, prefix="/api/v1/history", tags=["History"])
    app.include_router(targets.router, prefix="/api/v1/targets", tags=["Targets"])

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "name": "Zeron Web Security Testing Suite",
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


app = create_app()
