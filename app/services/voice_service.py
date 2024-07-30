from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Character, Chat
from app.models.bubble import Bubble
from app.models.voice import Voice
from app.schemas.voice import VoiceDetail
from app.config.redis.config import Config
from app.services import bubble_service

redis_client = Config.get_redis_client()


# 저장된 모든 목소리 목록 조회
def get_voices(db: Session, skip: int = 0, limit: int = 100):
    voices = db.query(Voice).filter(Voice.is_deleted == False).order_by(desc(Voice.created_at)).offset(skip).limit(limit).all()
    return [VoiceDetail(
        id=voice.id,
        chat_id=voice.bubble.chat_id,
        character=voice.bubble.chat.character.name,
        character_image=voice.bubble.chat.character.image_url,
        bubble_id=voice.bubble_id,
        audio_url=voice.audio_url,
        content=voice.content,
        created_at=voice.created_at
    ) for voice in voices]


# 채팅방 별 목소리 목록 조회
def get_voices_by_chat_id(db: Session, chat_id: int):
    voices = db.query(Voice).join(Voice.bubble).filter(Bubble.chat_id == chat_id, Voice.is_deleted == False).all()
    return [VoiceDetail(
        id=voice.id,
        chat_id=voice.bubble.chat_id,
        character=voice.bubble.chat.character.name,
        character_image=voice.bubble.chat.character.image_url,
        bubble_id=voice.bubble_id,
        audio_url=voice.audio_url,
        content=voice.content,
        created_at=voice.created_at
    ) for voice in voices]


# 단일 목소리 상세 조회
def get_voice_detail(db: Session, voice_id: int):
    voice = db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    return VoiceDetail(
        id=voice.id,
        chat_id=voice.bubble.chat_id,
        character=voice.bubble.chat.character.name,
        character_image=voice.bubble.chat.character.image_url,
        bubble_id=voice.bubble_id,
        audio_url=voice.audio_url,
        content=voice.content,
        created_at=voice.created_at
    )


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


# 사용자 선택 목소리 저장
def create_voice(db: Session, bubble_id: int, audio_url: str):
    bubble = bubble_service.get_bubble(db, bubble_id=bubble_id)
    if not bubble:
        raise HTTPException(status_code=404, detail="대화를 불러오는데 실패했습니다.")
    voice = Voice(bubble_id=bubble_id, content=bubble.content, audio_url=audio_url)
    db.add(voice)
    db.commit()
    db.refresh(voice)
    return VoiceDetail(
        id=voice.id,
        chat_id=bubble.chat_id,
        character=bubble.chat.character.name,
        character_image=bubble.chat.character.image_url,
        bubble_id=bubble_id,
        audio_url=audio_url,
        content=bubble.content,
        created_at=voice.created_at
    )


# 목소리 모델 가져오기
def get_voice(db: Session, voice_id: int):
    return db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()


# 목소리 카운트 증가시키기
def get_voice_count(db: Session, voice_id: int):
    voice = db.query(Voice).filter(Voice.id == voice_id, Voice.is_deleted == False).first()
    if voice:
        voice.v_count += 1
        db.commit()
        db.refresh(voice)


# 캐릭터 별 다운로드 횟수 기준으로 10개 출력
def get_top_voices_by_character(db: Session, character_id: int):
    return (db.query(Voice)
            .join(Voice.bubble)  # Image와 Bubble 간의 관계 조인
            .join(Bubble.chat)  # Bubble과 Chat 간의 관계 조인
            .join(Chat.character)  # Chat과 Character 간의 관계 조인
            .filter(Character.id == character_id, Voice.is_deleted == False)
            .order_by(desc(Voice.v_count))
            .limit(5)
            .all())
