import uuid

from fastapi import APIRouter

from app.schemas.schemas import ApiResponse, ApiRequestModel, ApiAssertRequest
from app.services.api_testing import api_service
from app.security.validation import ValidationError

router = APIRouter()


@router.post("/request", response_model=ApiResponse)
async def api_request(request: ApiRequestModel):
    request_id = str(uuid.uuid4())
    try:
        result = await api_service.send_request(request)
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


@router.post("/assert", response_model=ApiResponse)
async def api_assert(response_data: dict, assertions: ApiAssertRequest):
    request_id = str(uuid.uuid4())
    try:
        result = await api_service.assert_response(response_data, assertions)
        return ApiResponse(success=True, data=result, request_id=request_id)
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"code": "ASSERT_ERROR", "message": str(e)},
            request_id=request_id,
        )
