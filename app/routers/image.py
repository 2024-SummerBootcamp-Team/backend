from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.image import ImageBase
from app.database.session import get_db
from ..services import image_service
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

#@router.post("/images/{bubbleId}", response_model=ImageBase)
#def create_image (bubbleId: int, image: ImageCreate, db: Session = Depends(get_db)):
    #if not bubbleId or not image:
        #raise HTTPException(status_code=400, detail={"code": 400, "message": "필드 에러"})
    #db_image = create_image(db, bubbleId, image)
    #return {
        #"code": 200,
        #"message": "발췌 이미지를 생성했습니다.",
        #"data": db_image
    #}
@router.get("/{image_id}", response_model=ImageBase)
def get_image (image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    return image


