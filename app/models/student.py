"""Student database model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.progress import TopicProgress
    from app.models.submission import Submission


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    progress_records: Mapped[list[TopicProgress]] = relationship(
        "TopicProgress",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    submissions: Mapped[list[Submission]] = relationship(
        "Submission",
        back_populates="student",
        cascade="all, delete-orphan",
    )
