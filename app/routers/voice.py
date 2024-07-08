from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..services import voice_service, chat_service

from app.schemas.voice import VoiceBase

router = APIRouter(
    prefix="/voices",
    tags=["voices"],
    responses={404: {"description": "Not found"}},
)

# 저장한 목소리 목록 조회
@router.get("/chat/{chat_id}", response_model=List[VoiceBase])
def read_voices(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    voices = voice_service.get_voices(db, chat_id=chat_id)
    return voices

# 저장한 목소리 상세 조회
@router.get("/{voice_id}", response_model=VoiceBase)
def read_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    return voice
