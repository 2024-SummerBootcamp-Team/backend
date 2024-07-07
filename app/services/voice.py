from sqlalchemy.orm import Session

from app.models.voice import Voice


# 단일 목소리 상세 조회
def get_voice(db: Session, voice_id: int) -> Voice:
    return db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()
