import random
from io import BytesIO
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.config.elevenlabs.text_to_speech_stream import text_to_speech_stream
from app.config.redis.config import Config
from app.database.session import get_db
from app.models import Chat
from app.schemas.response import ResultResponseModel
from app.schemas.voice import VoiceCreateRequest
from app.services import bubble_service, voice_service, chat_service

router = APIRouter(
    prefix="/tests",
    tags=["Tests"]
)


# [TEST] tts 생성 테스트 - stream (임시)
@router.post("/tts/stream", summary="[TEST] TTS 생성 테스트", description="TTS를 생성한 후 스트리밍으로 반환합니다.")
def create_tts_stream(req: VoiceCreateRequest):
    audio_stream = text_to_speech_stream(req.content)
    return StreamingResponse(content=audio_stream, media_type="audio/mpeg")


# [TEST] TTS 생성 테스트 - websocket 연결 후 스트리밍 (임시)
# @router.websocket("/ws/text-to-speech", summary="[TEST] TTS 생성 테스트", description="TTS 생성 테스트 - websocket 연결 후 스트리밍으로 반환합니다.")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     text = await websocket.receive_text()
#
#     async for chunk in text_to_speech_stream(text):
#         print(chunk)
#         await websocket.send_bytes(chunk)


# [TEST] 버블아이디에 대한 tts 생성, 레디스 저장
@router.post("/redis/{bubble_id}", summary="[TEST] TTS 생성, 레디스 저장", description="버블아이디에 대한 TTS를 생성하고 레디스에 저장합니다.")  # 버블아이디에 대한 tts 생성하고 그걸 레디스에 저장하는것
async def create_tts_stream(bubble_id: int, db: Session = Depends(get_db)):
    bubble = bubble_service.get_bubble(db, bubble_id=bubble_id)
    if not bubble:
        raise HTTPException(status_code=404, detail="대화 정보를 불러오는데 실패했습니다.")
    # TTS 생성
    audio_data = text_to_speech_stream(bubble.content)
    # Redis에 저장할 고유 키 생성
    audio_key = f"{bubble_id}"
    # getvalue() 메서드는 BytesIO 객체에서 현재까지 읽은 데이터를 바이트열(bytes)로 반환
    audio_data_bytes = audio_data.getvalue()
    redis_client = Config.get_redis_client()
    # Redis에 오디오 데이터 저장
    redis_client.setex(audio_key, timedelta(seconds=600), audio_data_bytes)  # 생성과 동시에 10초뒤에 사라짐
    return ResultResponseModel(code=200, message="목소리가 Redis에 임시저장되었습니다.", data={"key": audio_key})


# [TEST] audio_key로 레디스에서 데이터 찾기
@router.get("/audio/{audio_key}", summary="[TEST] 레디스에서 TTS 찾기", description="audio_key로 레디스에서 TTS 음성 파일을 찾습니다.")
def get_tts(audio_key: str):
    try:
        audio_data = voice_service.get_voice_from_redis(audio_key)
        if audio_data is None:
            raise HTTPException(status_code=404, detail="해당 키로 데이터를 찾을 수 없습니다.")
        audio_stream = BytesIO(audio_data)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS 데이터를 가져오는데 실패했습니다: {str(e)}")


@router.get("/topic/{chat_id}", summary="[TEST] 채팅방 토픽 요약하기", description="채팅방의 최신 5개 버블을 통해 대화 주제를 요약합니다.")
def get_topic(chat_id: int, db: Session = Depends(get_db)):
    topic = chat_service.get_chat_topic(db, chat_id)
    return ResultResponseModel(code=200, message="topic을 반환합니다.", data={"topic": topic})
