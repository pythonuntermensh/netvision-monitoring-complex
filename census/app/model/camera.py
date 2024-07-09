from uuid import uuid4

from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from .models import Model


class Camera(Model):
    __tablename__ = 'camera'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    ip: Optional[str] = Column(String, default="192.168.0.1")
    port: Optional[int] = Column(Integer, default=0)
    login: Optional[str] = Column(String, default="")
    password: Optional[str] = Column(String, default="")
    status: Optional[int] = Column(Integer, default=0)
    group_uuid: UUID = Column(UUID, ForeignKey("group.uuid"), nullable=False, index=True)

    group = relationship("Group", back_populates="cameras")
