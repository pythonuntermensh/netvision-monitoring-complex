from typing import List

from fastapi import APIRouter, Depends

from model import Camera
from dto.request.statuses_update import StatusesUpdate
from data.camera import update_cameras_statuses

router = APIRouter(prefix="/statuses")


@router.post("/")
async def update_statuses(cameras_to_statuses: List[StatusesUpdate], result: None = Depends(update_cameras_statuses)) -> None:
    return result
