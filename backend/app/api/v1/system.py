import platform
import time

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.schemas import ApiResponse, HealthResponse, SystemInfo, SystemCapabilities

router = APIRouter()
settings = get_settings()
_start_time = time.time()


@router.get("/health", response_model=ApiResponse)
async def health_check():
    from app.adapters.cloudflare_adapter import cloudflare_adapter
    from app.adapters.recaptcha_adapter import recaptcha_adapter

    cf_health = await cloudflare_adapter.health_check()
    rec_health = await recaptcha_adapter.health_check()

    data = HealthResponse(
        status="healthy",
        version=settings.app_version,
        database="connected",
        browser=cf_health.get("status", "unavailable"),
        cloudflare=cf_health.get("status", "unavailable"),
        recaptcha=rec_health.get("status", "unavailable"),
    )
    return ApiResponse(success=True, data=data.model_dump())


@router.get("/system/info", response_model=ApiResponse)
async def system_info():
    import sys
    data = SystemInfo(
        app_name=settings.app_name,
        version=settings.app_version,
        python_version=sys.version,
        platform=platform.platform(),
        uptime_seconds=int(time.time() - _start_time),
        database_type=settings.database_url.split("://")[0] if "://" in settings.database_url else "sqlite",
    )
    return ApiResponse(success=True, data=data.model_dump())


@router.get("/system/capabilities", response_model=ApiResponse)
async def system_capabilities():
    data = SystemCapabilities(
        browser_enabled=settings.browser_enabled,
        cloudflare_enabled=settings.cloudflare_enabled,
        recaptcha_enabled=settings.recaptcha_enabled,
        supported_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
        max_request_size=settings.max_request_size,
        request_timeout=settings.request_timeout,
    )
    return ApiResponse(success=True, data=data.model_dump())
