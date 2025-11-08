from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TemplateCategory(str, enum.Enum):
    BUSINESS = "business"
    ECOMMERCE = "ecommerce"
    SAAS = "saas"
    DONATION = "donation"
    BLOG = "blog"


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    category = Column(Enum(TemplateCategory), nullable=False)
    version = Column(String, default="1.0.0")

    # Template structure
    config = Column(JSON, nullable=False)  # Template configuration
    layout_config = Column(JSON)  # Layout settings
    theme_config = Column(JSON)  # Theme variables
    content_schema = Column(JSON)  # Expected content structure

    # Metadata
    author = Column(String)
    preview_image = Column(String)
    tags = Column(JSON)  # List of tags
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)

    # Plugin hooks
    plugin_hooks = Column(JSON)  # Plugin integration points

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Template(name={self.name}, category={self.category})>"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)

    # Owner
    uploaded_by = Column(Integer, nullable=False)

    # Categorization
    asset_type = Column(String)  # image, document, video, etc.
    tags = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Asset(filename={self.filename}, type={self.mime_type})>"