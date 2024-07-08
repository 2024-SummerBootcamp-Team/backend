from sqlalchemy.orm import Session

from app.models.bubble import Bubble
from app.models.voice import Voice


# 목소리 목록 조회
def get_voices(db: Session, chat_id: int) -> list[Voice]:
    return db.query(Voice).join(Voice.bubble).filter(Bubble.chat_id == chat_id, Voice.is_deleted == False).all()

# 단일 목소리 상세 조회
def get_voice(db: Session, voice_id: int) -> Voice:
    return db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()

def delete_voice(db: Session, voice_id: int) -> None:
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if voice:
        db.delete(voice)
        db.commit()
