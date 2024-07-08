from fastapi import APIRouter
from . import chats
from . import voices

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chats.router)
router.include_router(voices.router)
