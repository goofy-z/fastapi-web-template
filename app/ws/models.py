import uuid

from app.models.base import Base
from sqlalchemy import Column, String


class Demo(Base):
    __tablename__ = "demos"
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    name = Column(String(128), nullable=False, primary_key=True, unique=True)
    description = Column(String(512), nullable=False)
