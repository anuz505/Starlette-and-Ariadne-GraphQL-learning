from sqlalchemy import DateTime, ForeignKey, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from .db_model import Base
from typing import Optional
from uuid import uuid4
from datetime import datetime
from .enums import PriorityEnum, StatusEnum


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[UUID] = mapped_column(ForeignKey("task.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[SAEnum[PriorityEnum]] = mapped_column(SAEnum[PriorityEnum], default=PriorityEnum.MEDIUM, nullable=False)
    