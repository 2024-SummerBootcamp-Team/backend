from fastapi import APIRouter
from .image import router as image_router

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(image_router)
