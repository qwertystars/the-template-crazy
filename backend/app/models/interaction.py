"""
Interaction model for comments, reviews, ratings, etc.
Uses generic relationships for flexibility.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class InteractionType(str, enum.Enum):
    """Interaction type enumeration."""
    COMMENT = "comment"
    REVIEW = "review"
    RATING = "rating"
    LIKE = "like"
    SHARE = "share"
    BOOKMARK = "bookmark"


class Interaction(Base):
    """Universal interaction model for user engagement."""

    __tablename__ = "interactions"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Interaction type
    interaction_type: Mapped[InteractionType] = mapped_column(
        SQLEnum(InteractionType, name="interaction_type"),
        nullable=False,
        index=True
    )

    # References
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    entity_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"),
        index=True
    )

    # Content
    content: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5 stars
    title: Mapped[Optional[str]] = mapped_column(String(255))

    # Status
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Flexible attributes
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

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="interactions")
    entity: Mapped[Optional["Entity"]] = relationship("Entity", back_populates="interactions")

    def __repr__(self) -> str:
        return f"<Interaction(id={self.id}, type={self.interaction_type}, user_id={self.user_id})>"
