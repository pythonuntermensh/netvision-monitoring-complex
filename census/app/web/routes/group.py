from fastapi import APIRouter, Depends
from typing import List

import uuid

from data.group import get_groups, create_group, delete_group_by_id
from model import Group
from dto.response import GroupOut
from dto.request import GroupCreate

router = APIRouter(prefix="/groups")


@router.get("/", response_model=List[GroupOut])
async def get_all_groups(groups: List[Group] = Depends(get_groups)) -> List[Group]:
    return groups


@router.post("/", response_model=GroupOut)
async def create_group(group_create: GroupCreate, group: Group = Depends(create_group)) -> Group:
    return group


@router.delete("/{group_id}")
async def delete_group(group_id: uuid.UUID, result: bool = Depends(delete_group_by_id)) -> bool:
    return result


