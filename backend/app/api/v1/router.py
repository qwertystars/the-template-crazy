"""
API v1 router - aggregates all endpoint routers.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, entities, transactions


# Create main API v1 router
api_router = APIRouter(prefix="/v1")

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(entities.router)
api_router.include_router(transactions.router)
