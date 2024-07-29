from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from ..schemas.response import ResultResponseModel
from ..services import image_service, chat_service, bubble_service
from app.config.aws.s3Client import upload_image
from app.schemas.image import ImageBase, ImageBaseList, ImageDetailList
from fastapi import File, UploadFile

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


# 저장된 모든 발췌 이미지 목록 조회
@router.get("", response_model=ResultResponseModel, summary="저장된 모든 발췌 이미지 목록 조회",
            description="DB에 저장된 모든 발췌 이미지 목록을 조회합니다.")
def read_images(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    images = image_service.get_images(db, skip=skip, limit=limit)
    return ResultResponseModel(code=200, message="저장된 모든 발췌 이미지 목록을 조회했습니다.", data=ImageDetailList(images=images))


# 발췌 이미지 저장
@router.post("/{bubble_id}", response_model=ResultResponseModel, summary="발췌 이미지 저장", description="발췌 이미지를 저장합니다.")
async def create_image(bubble_id: int, content: str = Form(...), file: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    valid_bubble_id = bubble_service.get_bubble(db, bubble_id=bubble_id)
    if not valid_bubble_id:
        raise HTTPException(status_code=404, detail="대화 정보를 불러오는데 실패했습니다.")
    try:
        image_url = await upload_image(file, file.content_type.split('/')[1])
    except Exception as e:
        raise HTTPException(status_code=500, detail="S3에 이미지 업로드 실패: {str(e)}")
    image = image_service.create_image(db, bubble_id=bubble_id, content=content, image_url=image_url)
    return ResultResponseModel(code=200, message="발췌 이미지를 저장하였습니다.", data=ImageBase.from_orm(image))


# 채팅방 별 저장한 발췌 이미지 목록 조회
@router.get("/chat/{chat_id}", response_model=ResultResponseModel, summary="채팅방 별 발췌 이미지 목록 조회",
            description="특정 채팅방에서 저장된 발췌 이미지 목록을 조회합니다.")
def read_images_in_chat_room(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    images = image_service.get_images_by_chat_id(db, chat_id=chat_id)
    return ResultResponseModel(code=200, message="채팅방 별 발췌 이미지 목록을 조회했습니다.", data=ImageBaseList(images=images))


# 저장한 발췌 이미지 상세 조회
@router.get("/{image_id}", response_model=ResultResponseModel, summary="발췌 이미지 상세 조회",
            description="특정 발췌 이미지의 상세 정보를 조회합니다.")
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    return ResultResponseModel(code=200, message="발췌 이미지 상세 정보를 조회했습니다.", data=ImageBase.from_orm(image))


# 저장한 발췌 이미지 소프트 삭제
@router.put("/{image_id}", response_model=ResultResponseModel, summary="발췌 이미지 소프트 삭제",
            description="특정 발췌 이미지를 삭제 처리합니다.")
def soft_delete_image(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    image_service.soft_delete_image(db, image_id=image_id)
    return ResultResponseModel(code=200, message="발췌 이미지를 삭제 처리했습니다.", data=None)


# 저장한 발췌 이미지 하드 삭제
@router.delete("/{image_id}", response_model=ResultResponseModel, summary="발췌 이미지 하드 삭제",
               description="특정 발췌 이미지를 DB에서 삭제합니다.")
def hard_delete_image(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="발췌 이미지 정보를 불러오는데 실패했습니다.")
    image_service.hard_delete_image(db, image_id=image_id)
    return ResultResponseModel(code=200, message="발췌 이미지를 DB에서 삭제했습니다.", data=None)


# 발췌 이미지 배경 목록 조회
@router.get("/samples/{character_name}", response_model=ResultResponseModel, summary="발췌 이미지 배경 목록 조회",
            description="발췌 이미지 생성 시 샘플로 제공되는 이미지 목록을 조회합니다.")
def read_samples(character_name: str, db: Session = Depends(get_db)):
    images = image_service.get_samples(db, character_name=character_name)
    return ResultResponseModel(code=200, message="샘플 배경 이미지 목록을 조회했습니다.", data=images)


# 이미지 다운로드 수
@router.post("/downloadcount/{image_id}", response_model=ResultResponseModel, summary="이미지 다운로드 수",
             description="이미지 다운로드 수를 알려줍니다.")
def download_image_count(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="이미지 정보를 불러오는데 실패했습니다.")
    image_service.get_image_count(db, image_id=image_id)
    return ResultResponseModel(code=200, message="이미지 카운트가 올라갔습니다.", data=image.i_count)
