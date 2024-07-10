from sqlalchemy.orm import Session

from app.models.bubble import Bubble
from app.models.voice import Voice
from app.schemas.voice import VoiceDetail
from app.config.redis.config import Config

redis_client = Config.get_redis_client()


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


# 저장한 목소리 하드 삭제
def hard_delete_voice(db: Session, voice_id: int, ) -> None:
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if voice:
        db.delete(voice)
        db.commit()


# 저장한 목소리 소프트 삭제
def soft_delete_voice(db: Session, voice_id: int) -> None:
    voice = db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()
    if voice:
        voice.is_deleted = True
        db.commit()


# audio_key로 레디스에서 목소리 데이터 찾기
def get_voice_from_redis(key: str):
    return redis_client.get(key)
