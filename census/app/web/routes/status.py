from typing import List

from fastapi import APIRouter, Depends

from depends import get_camera_service
from dto.request.statuses_update import StatusesUpdate
from service import CameraService

router = APIRouter(prefix="/statuses")


@router.post("/")
async def update_statuses(cameras_to_statuses: List[StatusesUpdate], service: CameraService = Depends(get_camera_service)) -> None:
    return service.update_cameras_statuses(cameras_to_statuses)
