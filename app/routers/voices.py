# from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, StreamingResponse
from starlette.websockets import WebSocket

from ..config.elevenlabs.text_to_speech_file import text_to_speech_file
from ..config.elevenlabs.text_to_speech_stream import text_to_speech_stream
from ..database.session import get_db
from ..services import voice_service, chat_service

from app.schemas.voice import VoiceBase, VoiceBaseList, VoiceDetailList, VoiceCreateRequest

router = APIRouter(
    prefix="/voices",
    tags=["voices"],
    responses={404: {"description": "Not found"}},
)


# 저장된 모든 목소리 목록 조회
@router.get("", response_model=VoiceDetailList)
def read_voices(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    voices = voice_service.get_voices(db, skip=skip, limit=limit)
    return VoiceDetailList(voices=voices)


# 채팅방 별 저장한 목소리 목록 조회
@router.get("/chat/{chat_id}", response_model=VoiceBaseList)
def read_voices_by_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    voices = voice_service.get_voices_by_chat_id(db, chat_id=chat_id)
    return VoiceBaseList(voices=voices)


# 저장한 목소리 상세 조회
@router.get("/{voice_id}", response_model=VoiceBase)
def read_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    return voice


@router.delete("/{voice_id}")
def hard_delete_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    voice_service.hard_delete_voice(db, voice_id=voice_id)


@router.put("/{voice_id}")
def soft_delete_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)

    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    voice_service.soft_delete_voice(db, voice_id=voice_id)
    return {
        "code": 200,
        "message": "TTS를 삭제했습니다.",
        "data": None  # or you can omit this line, as 'data' being None is default in the response_model
    }


# tts 생성 테스트
@router.post("/tts/file")
def create_tts_file(req: VoiceCreateRequest):
    file_path = text_to_speech_file(req.content)
    return FileResponse(file_path, media_type='audio/mpeg', filename=file_path.split("/")[-1])


@router.post("/tts/stream")
def create_tts_stream(req: VoiceCreateRequest):
    audio_stream = text_to_speech_stream(req.content)
    return StreamingResponse(content=audio_stream, media_type="audio/mpeg")



# @router.websocket("/ws/text-to-speech")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     text = await websocket.receive_text()
#
#     async for chunk in text_to_speech_stream(text):
#         await websocket.send_bytes(chunk)
