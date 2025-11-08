from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.template import Template, TemplateCategory
from app.schemas.template import Template as TemplateSchema, TemplateCreate, TemplateUpdate
from app.services.template_engine import TemplateEngine

router = APIRouter()


@router.get("/", response_model=List[TemplateSchema])
def list_templates(
    category: Optional[TemplateCategory] = Query(None, description="Filter by category"),
    is_active: bool = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of templates to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of templates to return"),
    db: Session = Depends(get_db)
):
    """List all templates with optional filtering"""
    query = db.query(Template).filter(Template.is_active == is_active)

    if category:
        query = query.filter(Template.category == category)

    templates = query.offset(skip).limit(limit).all()
    return templates


@router.get("/categories", response_model=List[str])
def list_template_categories():
    """List all available template categories"""
    return [category.value for category in TemplateCategory]


@router.get("/{template_id}", response_model=TemplateSchema)
def get_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template


@router.get("/slug/{slug}", response_model=TemplateSchema)
def get_template_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get a template by slug"""
    template = db.query(Template).filter(
        Template.slug == slug,
        Template.is_active == True
    ).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template


@router.post("/", response_model=TemplateSchema)
def create_template(
    template_create: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new template (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    template_engine = TemplateEngine(db)
    try:
        return template_engine.register_template(template_create.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{template_id}", response_model=TemplateSchema)
def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a template (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    for field, value in template_update.dict(exclude_unset=True).items():
        setattr(template, field, value)

    db.commit()
    db.refresh(template)
    return template


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a template (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    # Soft delete by setting is_active to False
    template.is_active = False
    db.commit()

    return {"message": "Template deleted successfully"}


@router.post("/{template_id}/validate-content")
def validate_content(
    template_id: int,
    content: dict,
    db: Session = Depends(get_db)
):
    """Validate content against template schema"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    template_engine = TemplateEngine(db)
    try:
        template_engine.validate_content_against_schema(content, template.content_schema)
        return {"valid": True}
    except ValueError as e:
        return {"valid": False, "error": str(e)}