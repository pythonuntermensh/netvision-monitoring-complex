from pydantic import BaseModel
from uuid import UUID


class CameraStatusOut(BaseModel):
    uuid: UUID
    status: int
