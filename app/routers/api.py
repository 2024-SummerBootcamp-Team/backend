from fastapi import APIRouter
from .chats import router as chats


router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chats)


