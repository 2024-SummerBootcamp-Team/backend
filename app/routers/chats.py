from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.response import ResultResponseModel
from ..services import chat_service
from ..database.session import get_db
from ..schemas.bubble import BubbleRequest
from ..schemas.chat import ChatRoomCreateRequest
from ..services import character_service
from ..services import bubble_service
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)


# 채팅방 생성
@router.post("", response_model=ResultResponseModel, summary="채팅방 생성", description="새로운 채팅방을 생성합니다.")
def create_chat_room(req: ChatRoomCreateRequest, db: Session = Depends(get_db)):
    character = character_service.get_character_by_name(db, character_name=req.character_name)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터 정보를 찾을 수 없습니다.")
    chat = chat_service.create_chat_room(db, chat_name=req.chat_room_name, character_id=character.id)
    if not chat:
        raise HTTPException(status_code=404, detail="채팅방 생성에 실패했습니다.")
    return ResultResponseModel(code=200, message="채팅방을 생성했습니다.", data={"chat_id": chat.id})


# 채팅하기: ai 답변 요청
@router.post("/{chat_id}", summary="대화 생성 - gpt", description="질문에 대한 gpt와의 답변을 텍스트와 TTS로 생성합니다.")
async def create_bubble(chat_id: int, req: BubbleRequest, db: Session = Depends(get_db)):
    chat_service.get_chat_room(db, chat_id=chat_id)
    try:
        response = StreamingResponse(bubble_service.create_bubble(db=db, chat_id=chat_id, content=req.content),
                                     media_type="text/event-stream")
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail="채팅하기에 실패했습니다.")


# 채팅방 정보 조회
@router.get("/{chat_id}", response_model=ResultResponseModel, summary="단일 채팅방 정보 조회",
            description="대화 내용을 제외한 채팅방에 대한 정보를 조회합니다.")
def read_chat_room(chat_id: int, db: Session = Depends(get_db)):
    chat = chat_service.get_chat_room(db, chat_id=chat_id)
    return ResultResponseModel(code=200, message="채팅방 정보를 조회했습니다.", data=chat)


# 전체 채팅 내용 조회
@router.get("/{chat_id}/bubbles", response_model=ResultResponseModel, summary="채팅 내용 조회",
            description="특정 채팅방의 모든 대화 내용을 조회합니다.")
def read_bubbles_in_chat_room(chat_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    chat_service.get_chat_room(db, chat_id=chat_id)
    bubbles = chat_service.get_bubbles(db, chat_id=chat_id, skip=skip, limit=limit)
    return ResultResponseModel(code=200, message="채팅방 전체 내용을 조회했습니다.", data=bubbles)
