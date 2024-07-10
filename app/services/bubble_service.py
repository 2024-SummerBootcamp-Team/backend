from sqlalchemy.orm import Session
from app.models import Bubble

def get_bubble(db: Session, bubble_id: int):
    return db.query(Bubble).filter(Bubble.id == bubble_id,Bubble.is_deleted == False).first()