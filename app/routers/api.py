from fastapi import APIRouter
from .chat_rooms import router as chat_rooms

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chat_rooms)