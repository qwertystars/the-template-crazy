from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.site import Site, Page
from app.schemas.site import Site as SiteSchema, SiteCreate, SiteUpdate, Page as PageSchema, PageCreate, PageUpdate

router = APIRouter()


@router.get("/", response_model=List[SiteSchema])
def list_sites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List user's sites"""
    query = db.query(Site).filter(Site.owner_id == current_user.id)
    sites = query.offset(skip).limit(limit).all()
    return sites


@router.post("/", response_model=SiteSchema)
def create_site(
    site_create: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new site"""
    site = Site(
        owner_id=current_user.id,
        **site_create.dict()
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/{site_id}", response_model=SiteSchema)
def get_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific site"""
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    return site


@router.put("/{site_id}", response_model=SiteSchema)
def update_site(
    site_id: int,
    site_update: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a site"""
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    for field, value in site_update.dict(exclude_unset=True).items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)
    return site


@router.delete("/{site_id}")
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a site"""
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    db.delete(site)
    db.commit()
    return {"message": "Site deleted successfully"}


# Pages endpoints
@router.get("/{site_id}/pages", response_model=List[PageSchema])
def list_site_pages(
    site_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List pages for a site"""
    # Verify site ownership
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    pages = db.query(Page).filter(Page.site_id == site_id).offset(skip).limit(limit).all()
    return pages


@router.post("/{site_id}/pages", response_model=PageSchema)
def create_page(
    site_id: int,
    page_create: PageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new page for a site"""
    # Verify site ownership
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check if slug is unique within the site
    existing_page = db.query(Page).filter(
        Page.site_id == site_id,
        Page.slug == page_create.slug
    ).first()
    if existing_page:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page slug must be unique within the site"
        )

    page = Page(
        site_id=site_id,
        **page_create.dict(exclude={"site_id"})
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.get("/{site_id}/pages/{page_id}", response_model=PageSchema)
def get_page(
    site_id: int,
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific page"""
    page = db.query(Page).join(Site).filter(
        Page.id == page_id,
        Page.site_id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    return page


@router.put("/{site_id}/pages/{page_id}", response_model=PageSchema)
def update_page(
    site_id: int,
    page_id: int,
    page_update: PageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a page"""
    page = db.query(Page).join(Site).filter(
        Page.id == page_id,
        Page.site_id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    # If updating slug, check uniqueness
    if page_update.slug and page_update.slug != page.slug:
        existing_page = db.query(Page).filter(
            Page.site_id == site_id,
            Page.slug == page_update.slug,
            Page.id != page_id
        ).first()
        if existing_page:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page slug must be unique within the site"
            )

    for field, value in page_update.dict(exclude_unset=True).items():
        setattr(page, field, value)

    db.commit()
    db.refresh(page)
    return page


@router.delete("/{site_id}/pages/{page_id}")
def delete_page(
    site_id: int,
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a page"""
    page = db.query(Page).join(Site).filter(
        Page.id == page_id,
        Page.site_id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    db.delete(page)
    db.commit()
    return {"message": "Page deleted successfully"}