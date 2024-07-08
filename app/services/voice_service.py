from sqlalchemy.orm import Session

from app.models.bubble import Bubble
from app.models.voice import Voice
from app.schemas.voice import VoiceDetail


# 저장된 모든 목소리 목록 조회
def get_voices(db: Session, skip: int = 0, limit: int = 100):
    voices = db.query(Voice).filter(Voice.is_deleted == False).offset(skip).limit(limit).all()
    voice_details = [VoiceDetail(
        id=voice.id,
        chat_id=voice.bubble.chat_id,
        character=voice.bubble.chat.character.name,
        bubble_id=voice.bubble_id,
        audio_url=voice.audio_url,
        content=voice.content,
        created_at=voice.created_at
    ) for voice in voices]
    return voice_details


# 채팅방 별 목소리 목록 조회
def get_voices_by_chat_id(db: Session, chat_id: int):
    return db.query(Voice).join(Voice.bubble).filter(Bubble.chat_id == chat_id, Voice.is_deleted == False).all()


# 단일 목소리 상세 조회
def get_voice(db: Session, voice_id: int):
    return db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()


def hard_delete_voice(db: Session, voice_id: int, ) -> None:
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if voice:
        db.delete(voice)
        db.commit()


def soft_delete_voice(db: Session, voice_id: int) -> None:
    voice = db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()
    if voice:
        voice.is_deleted = True
        db.commit()
