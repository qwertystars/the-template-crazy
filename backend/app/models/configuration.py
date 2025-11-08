"""
Configuration model for platform settings.
Stores platform configuration as JSON for flexibility.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class Configuration(Base):
    """Platform configuration storage."""

    __tablename__ = "configurations"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Configuration identification
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Configuration value (stored as JSON for flexibility)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<Configuration(key={self.key}, is_active={self.is_active})>"
