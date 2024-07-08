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


@router.get("/{image_id}", response_model=ImageBase)
def get_image (image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    return image


@router.delete("/{image_id}")
def hard_delete_image(image_id: int, db : Session = Depends(get_db)):
    image =  image_service.get_image(db, image_id=image_id )
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    image_service.hard_delete_image(db, image_id=image_id)

@router.put("/{image_id}")
def soft_delete_image (image_id: int, db : Session = Depends(get_db)):
        image = image_service.get_image(db, image_id)
        if not image:
            raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
        image_service.soft_delete_image(db, image_id=image_id)
        return {
            "code": 200,
            "message": "발췌 이미지를 삭제했습니다.",
            "data": None
        }



