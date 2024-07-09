from pydantic import BaseModel
from uuid import UUID


class CameraDetailedOut(BaseModel):
    uuid: UUID
    ip: str
    port: int
    login: str
    password: str
    status: int
    group_uuid: UUID
