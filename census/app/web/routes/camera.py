from fastapi import APIRouter, Depends
from typing import List

import uuid

from data.camera import get_cameras, get_camera_by_id, create_camera, delete_camera_by_id
from model import Camera
from dto.response import CameraOut, CameraDetailedOut
from dto.request import CameraCreate

router = APIRouter(prefix="/cameras")


@router.get("/", response_model=List[CameraOut])
async def get_all_cameras(cameras: List[Camera] = Depends(get_cameras)) -> List[Camera]:
    return cameras


@router.get("/{camera_id}", response_model=CameraDetailedOut)
async def get_camera(camera_id: uuid.UUID, camera: Camera = Depends(get_camera_by_id)) -> Camera:
    return camera


@router.post("/", response_model=CameraDetailedOut)
async def create_camera(camera_create: CameraCreate, camera: Camera = Depends(create_camera)) -> Camera:
    return camera


@router.delete("/{camera_id}")
async def delete_camera(camera_id: uuid.UUID, result: bool = Depends(delete_camera_by_id)) -> bool:
    return result




