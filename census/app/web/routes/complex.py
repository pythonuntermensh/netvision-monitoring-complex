from fastapi import APIRouter, Depends
from typing import List

import uuid

from depends import get_complex_service, get_camera_service
from dto.response import ComplexDetailedOut
from dto.response.complex_out import ComplexOut
from model import Complex
from dto.request import ComplexCreate
from service import ComplexService, CameraService

router = APIRouter(prefix="/complexes")


@router.get("/", response_model=List[ComplexOut])
async def get_all_complexes(service: ComplexService = Depends(get_complex_service)) -> List[Complex]:
    return service.get_complexes()


@router.get("/{complex_id}", response_model=ComplexDetailedOut)
async def get_complex(complex_id: uuid.UUID, service: ComplexService = Depends(get_complex_service)) -> Complex:
    return service.get_complex_by_id(complex_id)


@router.post("/", response_model=ComplexOut)
async def create_complex(complex_create: ComplexCreate, service: ComplexService = Depends(get_complex_service),
                         camera_service: CameraService = Depends(get_camera_service)) -> Complex:
    created_complex = service.create_complex(complex_create)

    service.create_cameras_in_complex(created_complex, camera_service)

    return created_complex


@router.delete("/{complex_id}")
async def delete_complex(complex_id: uuid.UUID, service: ComplexService = Depends(get_complex_service)) -> bool:
    return service.delete_complex_by_id(complex_id)
