import uuid

from fastapi import Depends
from typing import List

from sqlmodel import select
from sqlmodel import Session

from model import Group
from dto.request import GroupCreate
from config.db import get_session


def get_groups(session: Session = Depends(get_session)) -> List[Group]:
    result = session.scalars(select(Group)).all()
    return [Group(uuid=group.uuid, name=group.name) for group in result]


def create_group(group_create: GroupCreate, session: Session = Depends(get_session)) -> Group:
    new_group = Group(name=group_create.name)

    session.add(new_group)
    session.commit()
    session.refresh(new_group)

    return new_group


def delete_group_by_id(group_id: uuid.UUID, session: Session = Depends(get_session)) -> bool:
    result = session.get(Group, group_id)

    if result is None:
        return False

    session.delete(result)
    session.commit()
    return True
