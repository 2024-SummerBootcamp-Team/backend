from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from ..services import image_service, chat_service, bubble_service
from app.config.aws.s3Client import upload_image
from app.schemas.image import ImageBase, ImageBaseList, ImageDetailList
from pydantic import ValidationError
from ..schemas.image import ImageCreateRequest
from fastapi import FastAPI, File, UploadFile #fastapi에서 file과 uploadFile 임포트

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


# 저장된 모든 목소리 목록 조회
@router.get("", response_model=ImageDetailList)
def read_images(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    images = image_service.get_images(db, skip=skip, limit=limit)
    return ImageDetailList(images=images)


# 채팅방 별 저장한 목소리 목록 조회
@router.get("/chat/{chat_id}", response_model=ImageBaseList)
def read_images_by_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    images = image_service.get_images_by_chat_id(db, chat_id=chat_id)
    return ImageBaseList(images=images)

@router.get("/{image_id}", response_model=ImageBase)
def read_image (image_id: int, db: Session = Depends(get_db)):
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

@router.post("/{bubble_id}")
async def create_image_room (bubble_id: int, content: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    valid_bubble_id = bubble_service.get_bubble(db, bubble_id=bubble_id)

    if not valid_bubble_id:
        raise HTTPException(status_code=404, detail="대화 정보를 불러오는데 실패했습니다.")

    try:
        image_url = await upload_image(file, file.content_type.split('/')[1])
    except Exception as e:
        raise HTTPException(status_code=500, detail="S3에 이미지 업로드 실패: {str(e)}")

    image = image_service.create_image_room(db, bubble_id=bubble_id, content=content, image_url=image_url)

    return image