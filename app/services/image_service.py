from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.aws.s3Client import list_images_in_directory
from app.models import Bubble
from app.models.image import Image
from app.schemas.image import ImageDetail
from app.models.image import Image as ImageModel
from app.services import character_service


# 저장된 모든 발췌 이미지 목록 조회
def get_images(db: Session, skip: int = 0, limit: int = 100):
    images = db.query(Image).filter(Image.is_deleted == False).offset(skip).limit(limit).all()
    images_details = [ImageDetail(
        id=image.id,
        chat_id=image.bubble.chat_id,
        character=image.bubble.chat.character.name,
        bubble_id=image.bubble_id,
        image_url=image.image_url,
        content=image.content,
        created_at=image.created_at
    ) for image in images]
    return images_details


# 채팅방 별 목소리 목록 조회
def get_images_by_chat_id(db: Session, chat_id: int):
    return db.query(Image).join(Image.bubble).filter(Bubble.chat_id == chat_id, Image.is_deleted == False).all()


# 발췌 이미지 상세 조회
def get_image(db: Session, image_id: int) -> Image:
    return db.query(Image).filter(Image.id == image_id, Image.is_deleted == False).first()


# 발췌 이미지 하드 삭제
def hard_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()


# 발췌 이미지 소프트 삭제
def soft_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        image.is_deleted = True
        db.commit()


# 발췌 이미지 생성
def create_image(db: Session, bubble_id: int, content: str, image_url: str):
    image = ImageModel(bubble_id=bubble_id, content=content, image_url=image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


# 발췌 이미지 배경 목록 조회 - S3
def get_samples(db: Session, character_name: str):
    character = character_service.get_character_by_name(db, character_name)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터 정보를 불러오는데 실패했습니다.")
    images = list_images_in_directory(character_name)
    return images
