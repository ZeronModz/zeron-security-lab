import uuid
from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.schemas import ApiResponse, TargetCreate, TargetResponse

router = APIRouter()

_targets: dict[str, dict] = {}


@router.post("", response_model=ApiResponse)
async def create_target(request: TargetCreate):
    request_id = str(uuid.uuid4())
    target_id = str(uuid.uuid4())
    target = {
        "id": target_id,
        "url": request.url,
        "name": request.name,
        "description": request.description,
        "is_authorized": request.is_authorized,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _targets[target_id] = target
    return ApiResponse(success=True, data=target, request_id=request_id)


@router.get("", response_model=ApiResponse)
async def list_targets():
    request_id = str(uuid.uuid4())
    return ApiResponse(
        success=True,
        data={"targets": list(_targets.values()), "total": len(_targets)},
        request_id=request_id,
    )


@router.delete("/{target_id}", response_model=ApiResponse)
async def delete_target(target_id: str):
    request_id = str(uuid.uuid4())
    if target_id in _targets:
        del _targets[target_id]
        return ApiResponse(success=True, data={"deleted": True}, request_id=request_id)
    return ApiResponse(
        success=False,
        error={"code": "NOT_FOUND", "message": f"Target {target_id} not found"},
        request_id=request_id,
    )
