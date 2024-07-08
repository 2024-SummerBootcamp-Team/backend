from sqlalchemy.orm import Session

from app.models import Bubble
from app.models.image import Image
from app.schemas.image import ImageDetail


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


# 발췌 이미지 상세조회
def get_image(db: Session, image_id: int) -> Image:
    return db.query(Image).filter(Image.id == image_id, Image.is_deleted == False).first()


# 발췌 이미지 삭제
def hard_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()


def soft_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        image.is_deleted = True
        db.commit()
