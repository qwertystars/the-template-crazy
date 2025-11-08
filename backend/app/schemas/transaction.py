"""
Transaction Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.transaction import TransactionType, TransactionStatus


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""
    transaction_type: TransactionType
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    quantity: int = Field(default=1, gt=0)
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    user_id: Optional[int] = None
    entity_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    """Schema for updating transaction information."""
    status: Optional[TransactionStatus] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    user_id: Optional[int] = None
    entity_id: Optional[int] = None
    status: TransactionStatus
    total_amount: float
    payment_gateway: Optional[str] = None
    gateway_transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
