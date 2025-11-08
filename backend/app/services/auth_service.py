"""
Authentication service for user authentication and authorization.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, TokenData
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    """Service for handling authentication operations."""

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            Created user

        Raises:
            HTTPException: If email or username already exists
        """
        # Check if email already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username already exists (if provided)
        if user_data.username:
            result = await db.execute(
                select(User).where(User.username == user_data.username)
            )
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )

        # Create user
        hashed_pw = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pw,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            bio=user_data.bio,
            role=user_data.role,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, login_data: UserLogin
    ) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            db: Database session
            login_data: Login credentials

        Returns:
            User if authenticated, None otherwise
        """
        result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(login_data.password, user.hashed_password):
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()

        return user

    @staticmethod
    def create_tokens(user: User) -> Token:
        """
        Create access and refresh tokens for a user.

        Args:
            user: User to create tokens for

        Returns:
            Token response with access and refresh tokens
        """
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    async def get_current_user(db: AsyncSession, token: str) -> User:
        """
        Get current user from JWT token.

        Args:
            db: Database session
            token: JWT access token

        Returns:
            Current user

        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_token(token)
        if payload is None:
            raise credentials_exception

        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user
