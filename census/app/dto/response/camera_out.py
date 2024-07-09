from pydantic import BaseModel
from uuid import UUID


class CameraOut(BaseModel):
    uuid: UUID
    ip: str
    port: int
    status: int
    group_uuid: UUID
