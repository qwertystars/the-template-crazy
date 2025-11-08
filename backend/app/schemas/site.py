from typing import Optional, Dict, Any, List
from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime


class SiteBase(BaseModel):
    name: str
    domain: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    meta_description: Optional[str] = None
    favicon_url: Optional[str] = None
    google_analytics_id: Optional[str] = None
    custom_scripts: Optional[str] = None


class SiteCreate(SiteBase):
    config: Optional[Dict[str, Any]] = {}
    theme_config: Optional[Dict[str, Any]] = {}
    template_id: Optional[int] = None


class SiteUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    meta_description: Optional[str] = None
    favicon_url: Optional[str] = None
    google_analytics_id: Optional[str] = None
    custom_scripts: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    template_id: Optional[int] = None
    is_active: Optional[bool] = None


class Site(SiteBase):
    id: int
    owner_id: int
    template_id: Optional[int] = None
    config: Dict[str, Any]
    theme_config: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PageBase(BaseModel):
    title: str
    slug: str
    content: Dict[str, Any]
    is_published: bool = False
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class PageCreate(PageBase):
    site_id: int


class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class Page(PageBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True