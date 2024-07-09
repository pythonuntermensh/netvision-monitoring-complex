from pydantic import BaseModel
from uuid import UUID


class CameraCreate(BaseModel):
    ip: str
    port: int
    login: str
    password: str
    group_uuid: UUID
