import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.schemas import (
    ApiResponse,
    WebFetchRequest,
    WebFetchResponse,
    WebRenderRequest,
    WebRenderResponse,
    ScreenshotRequest,
    ScreenshotResponse,
    TestRunCreate,
    TestRunResponse,
)
from app.services.web_testing import web_service
from app.security.validation import ValidationError

router = APIRouter()


@router.post("/fetch", response_model=ApiResponse)
async def web_fetch(request: WebFetchRequest):
    request_id = str(uuid.uuid4())
    try:
        result = await web_service.fetch(request)
        return ApiResponse(success=True, data=result, request_id=request_id)
    except ValidationError as e:
        return ApiResponse(
            success=False,
            error={"code": e.code, "message": e.message},
            request_id=request_id,
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            request_id=request_id,
        )


@router.post("/render", response_model=ApiResponse)
async def web_render(request: WebRenderRequest):
    request_id = str(uuid.uuid4())
    try:
        result = await web_service.render(request)
        return ApiResponse(success=True, data=result, request_id=request_id)
    except ValidationError as e:
        return ApiResponse(
            success=False,
            error={"code": e.code, "message": e.message},
            request_id=request_id,
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            request_id=request_id,
        )


@router.post("/screenshot", response_model=ApiResponse)
async def web_screenshot(request: ScreenshotRequest):
    request_id = str(uuid.uuid4())
    try:
        result = await web_service.screenshot(request)
        return ApiResponse(success=True, data=result, request_id=request_id)
    except ValidationError as e:
        return ApiResponse(
            success=False,
            error={"code": e.code, "message": e.message},
            request_id=request_id,
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            request_id=request_id,
        )


@router.post("/tests", response_model=ApiResponse)
async def create_test(request: TestRunCreate):
    request_id = str(uuid.uuid4())
    test_run = {
        "id": str(uuid.uuid4()),
        "test_type": request.test_type,
        "target_url": request.target_url,
        "status": "completed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    return ApiResponse(success=True, data=test_run, request_id=request_id)


@router.get("/tests/{test_id}", response_model=ApiResponse)
async def get_test(test_id: str):
    request_id = str(uuid.uuid4())
    return ApiResponse(
        success=False,
        error={"code": "NOT_FOUND", "message": f"Test {test_id} not found"},
        request_id=request_id,
    )
