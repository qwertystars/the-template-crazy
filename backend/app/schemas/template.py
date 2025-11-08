from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
from app.models.template import TemplateCategory


class TemplateBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    category: TemplateCategory
    version: str = "1.0.0"
    author: Optional[str] = None
    preview_image: Optional[str] = None
    tags: Optional[List[str]] = []
    is_premium: bool = False


class TemplateCreate(TemplateBase):
    config: Dict[str, Any]
    layout_config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    content_schema: Optional[Dict[str, Any]] = None
    plugin_hooks: Optional[Dict[str, Any]] = None


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    layout_config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    content_schema: Optional[Dict[str, Any]] = None
    plugin_hooks: Optional[Dict[str, Any]] = None
    preview_image: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Template(TemplateBase):
    id: int
    config: Dict[str, Any]
    layout_config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    content_schema: Optional[Dict[str, Any]] = None
    plugin_hooks: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Asset(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    asset_type: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime

    class Config:
        orm_mode = True


class AssetUploadResponse(BaseModel):
    asset: Asset
    upload_url: Optional[str] = None