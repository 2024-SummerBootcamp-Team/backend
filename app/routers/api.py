from fastapi import APIRouter
from . import image
from . import chats
from . import voices

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(chats.router)
<<<<<<< HEAD
router.include_router(voice.router)
router.include_router(image.router)


=======
router.include_router(voices.router)
>>>>>>> 23b37cf49905fd1022efa82695360b12032d0747
