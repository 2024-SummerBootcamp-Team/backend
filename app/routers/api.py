from fastapi import APIRouter
from . import chats, voices, images, tests

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chats.router)
router.include_router(voices.router)
router.include_router(images.router)

router.include_router(tests.router)
