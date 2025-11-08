"""
Media model for file attachments and images.
Supports different media types with polymorphic relationships.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class MediaType(str, enum.Enum):
    """Media type enumeration."""
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"
    OTHER = "other"


class Media(Base):
    """Universal media storage model."""

    __tablename__ = "media"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Media type
    media_type: Mapped[MediaType] = mapped_column(
        SQLEnum(MediaType, name="media_type"),
        nullable=False,
        index=True
    )

    # File information
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)  # in bytes
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Image-specific attributes (if applicable)
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500))

    # Polymorphic relationship (can be attached to different entities)
    reference_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    reference_type: Mapped[Optional[str]] = mapped_column(String(50), index=True)

    # Additional metadata
    alt_text: Mapped[Optional[str]] = mapped_column(String(255))
    caption: Mapped[Optional[str]] = mapped_column(String(500))
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

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
        return f"<Media(id={self.id}, filename={self.filename}, type={self.media_type})>"
