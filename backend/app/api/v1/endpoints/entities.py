"""
Entity management endpoints for products, causes, etc.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.database import get_db
from app.models.entity import Entity, EntityType, EntityStatus
from app.models.user import User
from app.schemas.entity import EntityCreate, EntityUpdate, EntityResponse
from app.middleware.auth import get_current_active_user, get_current_user_optional, require_admin


router = APIRouter(prefix="/entities", tags=["Entities"])


@router.post("/", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity_data: EntityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Create a new entity (admin only).

    Args:
        entity_data: Entity creation data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Created entity

    Raises:
        HTTPException: If slug already exists
    """
    # Check if slug already exists
    result = await db.execute(
        select(Entity).where(Entity.slug == entity_data.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Entity with this slug already exists",
        )

    # Create entity
    db_entity = Entity(**entity_data.model_dump())
    db.add(db_entity)
    await db.commit()
    await db.refresh(db_entity)
    return db_entity


@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Get entity by ID.

    Args:
        entity_id: Entity ID
        db: Database session
        current_user: Optional current user

    Returns:
        Entity details

    Raises:
        HTTPException: If entity not found or not accessible
    """
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    # Only show active entities to non-admin users
    if entity.status != EntityStatus.ACTIVE:
        if not current_user or (not current_user.is_superuser and current_user.role.value != "admin"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found",
            )

    return entity


@router.get("/", response_model=List[EntityResponse])
async def list_entities(
    skip: int = 0,
    limit: int = 100,
    entity_type: Optional[EntityType] = None,
    status: Optional[EntityStatus] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    List entities with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        entity_type: Filter by entity type
        status: Filter by status
        search: Search in name and description
        db: Database session
        current_user: Optional current user

    Returns:
        List of entities
    """
    query = select(Entity)

    # Apply filters
    if entity_type:
        query = query.where(Entity.entity_type == entity_type)

    if status:
        query = query.where(Entity.status == status)
    elif not current_user or (not current_user.is_superuser and current_user.role.value != "admin"):
        # Non-admin users only see active entities
        query = query.where(Entity.status == EntityStatus.ACTIVE)

    if search:
        query = query.where(
            or_(
                Entity.name.ilike(f"%{search}%"),
                Entity.description.ilike(f"%{search}%"),
            )
        )

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    entities = result.scalars().all()
    return entities


@router.put("/{entity_id}", response_model=EntityResponse)
async def update_entity(
    entity_id: int,
    entity_update: EntityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Update entity (admin only).

    Args:
        entity_id: Entity ID
        entity_update: Entity update data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Updated entity

    Raises:
        HTTPException: If entity not found
    """
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    # Update fields
    update_data = entity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entity, field, value)

    await db.commit()
    await db.refresh(entity)
    return entity


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(
    entity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Delete entity (admin only).

    Args:
        entity_id: Entity ID to delete
        db: Database session
        current_user: Current authenticated admin user

    Raises:
        HTTPException: If entity not found
    """
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    await db.delete(entity)
    await db.commit()
