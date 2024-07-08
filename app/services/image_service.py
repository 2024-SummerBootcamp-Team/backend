from sqlalchemy.orm import Session

from app.models.image import Image

#발췌 이미지 상세조회
def get_image(db: Session, image_id: int) -> Image:
    return db.query(Image).filter(Image.id == image_id, Image.is_deleted == False).first()

#발췌 이미지 삭제
def hard_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()

def soft_delete_image(db: Session, image_id: int) -> None:
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        image.is_deleted=True
        db.commit()
