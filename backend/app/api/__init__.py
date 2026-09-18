from fastapi import APIRouter
from .recipes import router as recipes_router
from .tags import router as tags_router

api_router = APIRouter()
api_router.include_router(recipes_router)
api_router.include_router(tags_router)

__all__ = ["api_router"]