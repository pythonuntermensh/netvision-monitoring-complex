import uuid

from fastapi import Depends
from typing import List

from sqlmodel import select
from sqlmodel import Session

from model import Camera
from dto.request import CameraCreate, StatusesUpdate
from config.db import get_session


def get_cameras(session: Session = Depends(get_session)) -> List[Camera]:
    result = session.scalars(select(Camera)).all()
    return [Camera(uuid=camera.uuid,
                   ip=camera.ip,
                   port=camera.port,
                   login=camera.login,
                   password=camera.password,
                   status=camera.status,
                   group_uuid=camera.group_uuid) for camera in result]


def get_camera_by_id(camera_id: uuid.UUID, session: Session = Depends(get_session)) -> Camera:
    result = session.get(Camera, camera_id)
    return result


def create_camera(camera_create: CameraCreate, session: Session = Depends(get_session)) -> Camera:
    new_camera = Camera(ip=camera_create.ip,
                        port=camera_create.port,
                        login=camera_create.login,
                        password=camera_create.password,
                        group_uuid=camera_create.group_uuid)

    session.add(new_camera)
    session.commit()
    session.refresh(new_camera)

    return new_camera


def delete_camera_by_id(camera_id: uuid.UUID, session: Session = Depends(get_session)) -> bool:
    result = session.get(Camera, camera_id)

    if result is None:
        return False

    session.delete(result)
    session.commit()
    return True


def update_cameras_statuses(cameras_to_statuses: List[StatusesUpdate], session: Session = Depends(get_session)) -> None:
    for pair in cameras_to_statuses:
        camera = session.get(Camera, pair.uuid)
        camera.status = pair.status
        session.commit()


