from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.image_service import create_image, get_image, get_images_by_bubble_id
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageResponse, Image
from app.database.session import get_db
router = APIRouter()
@router.post("/images/{bubbleId}", response_model=ImageResponse)
def create_image (bubbleId: int, image: ImageCreate, db: Session = Depends(get_db)):
    if not bubbleId or not image:
        raise HTTPException(status_code=400, detail={"code": 400, "message": "필드 에러"})
    db_image = create_image(db, bubbleId, image)
    return {
        "code": 200,
        "message": "발췌 이미지를 생성했습니다.",
        "data": db_image
    }
@router.get("/images/{imageId}", response_model=ImageResponse)
def get_image (imageId: int, db: Session = Depends(get_db)):
    if not imageId:
        raise HTTPException(status_code=400, detail={"code": 400, "message": "필드 에러"})
    db_image = get_image(db, imageId)
    if db_image is None:
        raise HTTPException(status_code=404, detail={"code": 404, "message": "발췌 이미지를 정보를 불러오는데 실패했습니다."})
    return {
        "code": 200,
        "message": "발췌 이미지를 조회했습니다.",
        "data": db_image
    }



