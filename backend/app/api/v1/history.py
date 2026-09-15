import uuid

from fastapi import APIRouter

from app.schemas.schemas import ApiResponse, HistoryEntry

router = APIRouter()


@router.get("", response_model=ApiResponse)
async def get_history():
    request_id = str(uuid.uuid4())
    return ApiResponse(
        success=True,
        data={"entries": [], "total": 0, "page": 1, "per_page": 20},
        request_id=request_id,
    )
