"""
User model with role-based fields.
Supports multiple user types: customer, donor, subscriber, admin, beneficiary.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    CUSTOMER = "customer"
    DONOR = "donor"
    SUBSCRIBER = "subscriber"
    BENEFICIARY = "beneficiary"
    GUEST = "guest"


class User(Base):
    """Universal user model supporting multiple platform types."""

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Profile
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Role and permissions
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"),
        default=UserRole.CUSTOMER,
        nullable=False
    )

    # Flexible attributes for different use cases
    # Examples: preferences, addresses, payment methods, social profiles, etc.
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
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
