from fastapi import APIRouter
from .chats import router as chat_rooms
from .bubbles import router as bubble_rooms

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chat_rooms)
router.include_router(bubble_rooms)