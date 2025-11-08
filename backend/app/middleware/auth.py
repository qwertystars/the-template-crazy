"""
Authentication middleware and dependencies.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth_service import AuthService


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        credentials: HTTP authorization credentials
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    user = await AuthService.get_current_user(db, token)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: Current user from token

    Returns:
        Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependency to get the current verified user.

    Args:
        current_user: Current active user

    Returns:
        Current verified user

    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )
    return current_user


def require_role(required_role: UserRole):
    """
    Dependency factory to require a specific user role.

    Args:
        required_role: Required user role

    Returns:
        Dependency function
    """

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        """Check if user has required role."""
        if current_user.role != required_role and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role.value}",
            )
        return current_user

    return role_checker


async def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependency to require admin user.

    Args:
        current_user: Current active user

    Returns:
        Admin user

    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_superuser and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# Optional authentication - doesn't raise exception if no token
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Dependency to optionally get the current user.
    Returns None if no valid token is provided.

    Args:
        credentials: Optional HTTP authorization credentials
        db: Database session

    Returns:
        Current user or None
    """
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        user = await AuthService.get_current_user(db, token)
        return user
    except HTTPException:
        return None
