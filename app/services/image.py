from sqlalchemy.orm import Session
from app.models.image import Image as ImageModel
from app.schemas.image import ImageCreate

def create_image(db: Session, bubble_id: int, image: ImageCreate) -> ImageModel:
    db_image = ImageModel(**image.dict(), chatbubble_id=bubble_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: int) -> ImageModel:
    return db.query(ImageModel).filter(ImageModel.id == image_id).first()

def get_images_by_bubble_id(db: Session, bubble_id: int) -> list[ImageModel]:
    return db.query(ImageModel).filter(ImageModel.chatbubble_id == bubble_id).all()
