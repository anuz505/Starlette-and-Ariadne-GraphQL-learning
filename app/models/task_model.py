from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db_model import Base
from typing import Optional
from uuid import uuid4
from datetime import datetime
from .enums import PriorityEnum, StatusEnum, RoleEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum, name="role_enum"), default=RoleEnum.project_manager, nullable=False)

    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="assignee")

    __table_args__ = (CheckConstraint("length(password) >= 8", name="password_at_least_8_chars"),)


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    owner: Mapped["User"] = relationship("User", back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[PriorityEnum] = mapped_column(SAEnum(PriorityEnum, name="priority_enum"), default=PriorityEnum.MEDIUM, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SAEnum(StatusEnum, name="status_enum"), default=StatusEnum.TODO, nullable=False)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assignee_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    assignee: Mapped[Optional["User"]] = relationship("User", back_populates="tasks")
