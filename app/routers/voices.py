from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from io import BytesIO

from ..database.session import get_db
from ..services import voice_service, chat_service, bubble_service
from ..schemas.response import ResultResponseModel
from app.config.aws.s3Client import upload_voice

from app.schemas.voice import VoiceDetail, VoiceDetailList

router = APIRouter(
    prefix="/voices",
    tags=["Voices"]
)


# 저장된 모든 목소리 목록 조회
@router.get("", response_model=ResultResponseModel, summary="저장된 모든 목소리 목록 조회", description="DB에 저장된 모든 목소리 목록을 조회합니다.")
def read_voices(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    voices = voice_service.get_voices(db, skip=skip, limit=limit)
    return ResultResponseModel(code=200, message="저장된 모든 목소리 목록을 조회했습니다.", data=VoiceDetailList(voices=voices))


# 사용자 선택 목소리 저장
@router.post("/{bubble_id}", summary="사용자가 선택한 목소리 저장", description="대화 중 사용자가 선택한 목소리를 DB에 저장합니다.")
async def create_voice(bubble_id: int, db: Session = Depends(get_db)):
    bubble = bubble_service.get_bubble(db, bubble_id=bubble_id)
    if not bubble:
        raise HTTPException(status_code=404, detail="대화를 불러오는데 실패했습니다.")
    audio_key = f"{bubble_id}"
    audio_data = voice_service.get_voice_from_redis(audio_key)
    if not audio_data:
        raise HTTPException(status_code=404, detail="Redis에 음성 데이터 없음")
    try:
        file = BytesIO(audio_data)
        audio_url = await upload_voice(file)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="실패")
    voice = voice_service.create_voice(db, bubble_id=bubble_id, audio_url=audio_url)
    return voice


# 채팅방 별 저장한 목소리 목록 조회
@router.get("/chat/{chat_id}", response_model=ResultResponseModel, summary="채팅방 별 목소리 목록 조회",
            description="특정 채팅방에서 저장된 목소리 목록을 조회합니다.")
def read_voices_in_chat_room(chat_id: int, db: Session = Depends(get_db)):
    chat_service.get_chat_room(db, chat_id=chat_id)
    voices = voice_service.get_voices_by_chat_id(db, chat_id=chat_id)
    return ResultResponseModel(code=200, message="채팅방 별 목소리 목록을 조회했습니다.", data=VoiceDetailList(voices=voices))


# 저장한 목소리 상세 조회
@router.get("/{voice_id}", response_model=ResultResponseModel, summary="저장한 목소리 상세 조회",
            description="특정 목소리의 상세 정보를 조회합니다.")
def read_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice_detail(db, voice_id=voice_id)
    return ResultResponseModel(code=200, message="목소리 상세 정보를 조회했습니다.", data=voice)


# 저장한 목소리 소프트 삭제
@router.put("/{voice_id}", summary="목소리 소프트 삭제", description="특정 목소리를 삭제 처리합니다.")
def soft_delete_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    voice_service.soft_delete_voice(db, voice_id=voice_id)
    return ResultResponseModel(code=200, message="목소리를 삭제 처리했습니다.", data=None)


# 저장한 목소리 하드 삭제
@router.delete("/{voice_id}", response_model=ResultResponseModel, summary="목소리 하드 삭제",
               description="특정 목소리를 DB에서 삭제합니다.")
def hard_delete_voice(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    voice_service.hard_delete_voice(db, voice_id=voice_id)
    return ResultResponseModel(code=200, message="목소리를 DB에서 삭제했습니다.", data=None)


#목소리 다운로드 수
@router.post("/count/{voice_id}", response_model=ResultResponseModel, summary="목소리 다운로드 수",
             description="목소리 다운로드 수를 알려줍니다")
def download_voice_count(voice_id: int, db: Session = Depends(get_db)):
    voice = voice_service.get_voice(db, voice_id=voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="목소리 정보를 불러오는데 실패했습니다.")
    voice_service.get_voice_count(db, voice_id=voice_id)
    return ResultResponseModel(code=200, message="목소리 카운트가 올라갔습니다.", data=voice.v_count)
