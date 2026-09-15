import uuid

from fastapi import APIRouter

from app.schemas.schemas import (
    ApiResponse,
    CloudflareTestRequest,
    CloudflareTestResponse,
    RecaptchaTestRequest,
    RecaptchaTestResponse,
)
from app.adapters.cloudflare_adapter import cloudflare_adapter
from app.adapters.recaptcha_adapter import recaptcha_adapter

router = APIRouter()


@router.get("/cloudflare/health", response_model=ApiResponse)
async def cloudflare_health():
    request_id = str(uuid.uuid4())
    health = await cloudflare_adapter.health_check()
    return ApiResponse(success=True, data=health, request_id=request_id)


@router.post("/cloudflare/test", response_model=ApiResponse)
async def cloudflare_test(request: CloudflareTestRequest):
    request_id = str(uuid.uuid4())
    result = await cloudflare_adapter.test_url(
        url=request.url,
        proxy=request.proxy,
        timeout=request.timeout,
    )
    return ApiResponse(success=result["success"], data=result, request_id=request_id)


@router.post("/cloudflare/html", response_model=ApiResponse)
async def cloudflare_html(request: CloudflareTestRequest):
    request_id = str(uuid.uuid4())
    result = await cloudflare_adapter.get_html(url=request.url, proxy=request.proxy)
    return ApiResponse(success=result["success"], data=result, request_id=request_id)


@router.post("/cloudflare/cookies", response_model=ApiResponse)
async def cloudflare_cookies(request: CloudflareTestRequest):
    request_id = str(uuid.uuid4())
    result = await cloudflare_adapter.get_cookies(url=request.url, proxy=request.proxy)
    return ApiResponse(success=result["success"], data=result, request_id=request_id)


@router.get("/recaptcha/health", response_model=ApiResponse)
async def recaptcha_health():
    request_id = str(uuid.uuid4())
    health = await recaptcha_adapter.health_check()
    return ApiResponse(success=True, data=health, request_id=request_id)


@router.post("/recaptcha/test", response_model=ApiResponse)
async def recaptcha_test(request: RecaptchaTestRequest):
    request_id = str(uuid.uuid4())
    result = await recaptcha_adapter.test_recaptcha(
        url=request.url,
        site_key=request.site_key,
        timeout=request.timeout,
    )
    return ApiResponse(success=result["success"], data=result, request_id=request_id)


@router.post("/recaptcha/verify", response_model=ApiResponse)
async def recaptcha_verify(token: str, secret_key: str | None = None):
    request_id = str(uuid.uuid4())
    result = await recaptcha_adapter.verify_token(token=token, secret_key=secret_key)
    return ApiResponse(success=result["success"], data=result, request_id=request_id)
