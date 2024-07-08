from sqlalchemy.orm import Session

from app.models.image import Image


#발췌 이미지 생성
#def create_image(db: Session, bubble_id: int, image: ImageCreate) -> Image:
    #db_image = Image(**image.dict(), chatbubble_id=bubble_id)
    #db.add(db_image)
    #db.commit()
    #db.refresh(db_image)
    #return db_image

#발췌 이미지 상세조회
def get_image(db: Session, image_id: int) -> Image:
    return db.query(Image).filter(Image.id == image_id, Image.is_deleted == False).first()

