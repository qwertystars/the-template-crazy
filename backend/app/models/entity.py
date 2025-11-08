"""
Entity model for abstract content items.
Supports products, causes, subscription tiers, resources, etc.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Numeric, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class EntityType(str, enum.Enum):
    """Entity type enumeration."""
    PRODUCT = "product"
    CAUSE = "cause"
    SUBSCRIPTION_TIER = "subscription_tier"
    RESOURCE = "resource"
    SERVICE = "service"
    EVENT = "event"


class EntityStatus(str, enum.Enum):
    """Entity status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Entity(Base):
    """Universal entity model for different content types."""

    __tablename__ = "entities"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Type and status
    entity_type: Mapped[EntityType] = mapped_column(
        SQLEnum(EntityType, name="entity_type"),
        nullable=False,
        index=True
    )
    status: Mapped[EntityStatus] = mapped_column(
        SQLEnum(EntityStatus, name="entity_status"),
        default=EntityStatus.DRAFT,
        nullable=False
    )

    # Basic information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    short_description: Mapped[Optional[str]] = mapped_column(String(500))

    # Pricing (applicable for products, subscription tiers)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    compare_at_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    # Inventory (for products)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    track_inventory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allow_backorder: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Media
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    gallery: Mapped[Optional[list]] = mapped_column(JSONB, default=list)

    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(String(255))
    meta_description: Mapped[Optional[str]] = mapped_column(String(500))

    # Flexible attributes for different entity types
    # Examples: features, specifications, goals, perks, requirements, etc.
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
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="entity"
    )
    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction",
        back_populates="entity",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Entity(id={self.id}, name={self.name}, type={self.entity_type})>"
