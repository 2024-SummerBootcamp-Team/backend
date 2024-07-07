from sqlalchemy.orm import Session
from app.models.image import Image as ImageModel
from app.schemas.image import ImageCreate

def create_image(db: Session, bubble_id: int, image: ImageCreate) -> ImageModel:
    # ImageCreate 타입의 객체 image와 int 타입의 bubble_id, 그리고 SQLAlchemy의 Session 객체 db를 인자로 받습니다.
    # ImageCreate 객체 image를 딕셔너리로 변환하고, chatbubble_id 필드에 bubble_id 값을 추가하여 ImageModel 인스턴스를 생성합니다.
    db_image = ImageModel(**image.dict(), chatbubble_id=bubble_id)
    # 생성된 db_image 객체를 세션에 추가합니다.
    db.add(db_image)
    # 세션의 변경사항을 커밋하여 데이터베이스에 반영합니다.
    db.commit()
    # 데이터베이스에 반영된 db_image 객체를 새로 고칩니다 (갱신된 정보를 가져옵니다).
    db.refresh(db_image)
    # 갱신된 db_image 객체를 반환합니다.
    return db_image

def get_image(db: Session, image_id: int) -> ImageModel:
    return db.query(ImageModel).filter(ImageModel.id == image_id).first()

def get_images_by_bubble_id(db: Session, bubble_id: int) -> list[ImageModel]:
    return db.query(ImageModel).filter(ImageModel.chatbubble_id == bubble_id).all()
