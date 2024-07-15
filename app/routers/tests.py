import io
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.config.elevenlabs.text_to_speech_stream import text_to_speech_stream
from app.config.redis.config import Config
from app.database.session import get_db
from app.schemas.response import ResultResponseModel
from app.schemas.voice import VoiceCreateRequest
from app.services import bubble_service, voice_service

router = APIRouter(
    prefix="/tests",
    tags=["tests"],

    responses={404: {"description": "Not found"}},
)


# [TEST]  tts 생성 테스트 - stream (임시)
@router.post("/tts/stream")
def create_tts_stream(req: VoiceCreateRequest):
    audio_stream = text_to_speech_stream(req.content)
    return StreamingResponse(content=audio_stream, media_type="audio/mpeg")


# # tts 생성 테스트 - websocket 연결 후 스트리밍 (임시)
# @router.websocket("/ws/text-to-speech")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     text = await websocket.receive_text()
#
#     async for chunk in text_to_speech_stream(text):
#         print(chunk)
#         await websocket.send_bytes(chunk)


# [TEST] 버블아이디에 대한 tts 생성, 레디스 저장
@router.post("/redis/{bubble_id}")  # 버블아이디에 대한 tts 생성하고 그걸 레디스에 저장하는것
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
@router.get("/audio/{audio_key}")
def get_tts(audio_key: str):
    try:
        audio_data = voice_service.get_voice_from_redis(audio_key)
        if audio_data is None:
            raise HTTPException(status_code=404, detail="해당 키로 데이터를 찾을 수 없습니다.")
        audio_stream = io.BytesIO(audio_data)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS 데이터를 가져오는데 실패했습니다: {str(e)}")