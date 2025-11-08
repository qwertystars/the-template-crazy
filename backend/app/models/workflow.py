"""
Workflow model for state machines.
Tracks different processes and their states.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.database import Base


class WorkflowType(str, enum.Enum):
    """Workflow type enumeration."""
    ORDER_FULFILLMENT = "order_fulfillment"
    DONATION_PROCESSING = "donation_processing"
    SUBSCRIPTION_LIFECYCLE = "subscription_lifecycle"
    USER_ONBOARDING = "user_onboarding"
    CONTENT_APPROVAL = "content_approval"


class WorkflowStatus(str, enum.Enum):
    """Workflow status enumeration."""
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workflow(Base):
    """State machine tracking for different processes."""

    __tablename__ = "workflows"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Workflow type and status
    workflow_type: Mapped[WorkflowType] = mapped_column(
        SQLEnum(WorkflowType, name="workflow_type"),
        nullable=False,
        index=True
    )
    status: Mapped[WorkflowStatus] = mapped_column(
        SQLEnum(WorkflowStatus, name="workflow_status"),
        default=WorkflowStatus.INITIATED,
        nullable=False,
        index=True
    )

    # Current state in the workflow
    current_state: Mapped[str] = mapped_column(String(100), nullable=False)

    # References (polymorphic - can reference different entities)
    reference_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))

    # Workflow data
    data: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

    # History of state transitions
    history: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(Text)

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

    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, type={self.workflow_type}, status={self.status})>"
