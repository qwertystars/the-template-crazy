from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, sites, templates

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])