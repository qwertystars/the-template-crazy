from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Configuration
    config = Column(JSON)  # Site configuration data
    theme_config = Column(JSON)  # Theme customization

    # SEO
    title = Column(String)
    meta_description = Column(String)
    favicon_url = Column(String)

    # Analytics
    google_analytics_id = Column(String)
    custom_scripts = Column(Text)  # Header/footer scripts

    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"))

    owner = relationship("User", back_populates="sites")
    template = relationship("Template", back_populates="sites")
    pages = relationship("Page", back_populates="site", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Site(name={self.name}, domain={self.domain})>"


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, index=True)
    content = Column(JSON)  # Page content structure
    is_published = Column(Boolean, default=False)

    # SEO
    meta_title = Column(String)
    meta_description = Column(String)

    # Relationships
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site", back_populates="pages")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Page(title={self.title}, slug={self.slug})>"