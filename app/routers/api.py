import logging

from fastapi import APIRouter
from . import chats, voices, images, tests, characters
from .logging import LoggingRoute

# from .logging import LoggingRoute


router = APIRouter(
    route_class=LoggingRoute,
    prefix="/api/v1"
)

logging.basicConfig(
    filename='logs/app.log',  # 로그 파일 이름
    level=logging.DEBUG,  # 로그 레벨
    filemode="a",
    format='%(asctime)s %(levelname)s %(message)s'  # 로그 메시지 포맷
)


router.include_router(characters.router)
router.include_router(chats.router)
router.include_router(voices.router)
router.include_router(images.router)

router.include_router(tests.router)
