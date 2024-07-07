from fastapi import APIRouter
from . import chats
from . import voice

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chats.router)
router.include_router(voice.router)
