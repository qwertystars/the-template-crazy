"""
Entity Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.entity import EntityType, EntityStatus


class EntityBase(BaseModel):
    """Base entity schema with common fields."""
    entity_type: EntityType
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"
    compare_at_price: Optional[float] = None
    stock_quantity: int = 0
    track_inventory: bool = True
    allow_backorder: bool = False
    image_url: Optional[str] = None
    gallery: Optional[list] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    metadata: Optional[dict] = None


class EntityCreate(EntityBase):
    """Schema for creating a new entity."""
    status: EntityStatus = EntityStatus.DRAFT


class EntityUpdate(BaseModel):
    """Schema for updating entity information."""
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = None
    compare_at_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    track_inventory: Optional[bool] = None
    allow_backorder: Optional[bool] = None
    image_url: Optional[str] = None
    gallery: Optional[list] = None
    status: Optional[EntityStatus] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    metadata: Optional[dict] = None


class EntityResponse(EntityBase):
    """Schema for entity response."""
    id: int
    status: EntityStatus
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
