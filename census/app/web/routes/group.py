from fastapi import APIRouter, Depends
from typing import List

import uuid

from depends import get_group_service
from model import Group
from dto.response import GroupOut
from dto.request import GroupCreate
from service import GroupService

router = APIRouter(prefix="/groups")


@router.get("/", response_model=List[GroupOut])
async def get_all_groups(service: GroupService = Depends(get_group_service)) -> List[Group]:
    return service.get_groups()


@router.post("/", response_model=GroupOut)
async def create_group(group_create: GroupCreate, service: GroupService = Depends(get_group_service)) -> Group:
    return service.create_group(group_create)


@router.delete("/{group_id}")
async def delete_group(group_id: uuid.UUID, service: GroupService = Depends(get_group_service)) -> bool:
    return service.delete_group_by_id(group_id)
