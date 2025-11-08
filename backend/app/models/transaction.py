"""
Transaction model for universal transaction logging.
Supports purchases, donations, subscriptions, allocations, etc.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Integer, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    PURCHASE = "purchase"
    DONATION = "donation"
    SUBSCRIPTION = "subscription"
    REFUND = "refund"
    ALLOCATION = "allocation"
    PAYMENT = "payment"


class TransactionStatus(str, enum.Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Transaction(Base):
    """Universal transaction model for different payment types."""

    __tablename__ = "transactions"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Transaction type and status
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type"),
        nullable=False,
        index=True
    )
    status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(TransactionStatus, name="transaction_status"),
        default=TransactionStatus.PENDING,
        nullable=False,
        index=True
    )

    # References
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    entity_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("entities.id", ondelete="SET NULL"),
        index=True
    )

    # Financial details
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    tax_amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    discount_amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Payment gateway information
    payment_method: Mapped[Optional[str]] = mapped_column(String(50))
    payment_gateway: Mapped[Optional[str]] = mapped_column(String(50))
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    gateway_response: Mapped[Optional[dict]] = mapped_column(JSONB)

    # Additional information
    description: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    # Flexible attributes for different transaction types
    # Examples: shipping info, recurring details, allocation targets, etc.
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
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="transactions")
    entity: Mapped[Optional["Entity"]] = relationship("Entity", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.total_amount})>"
