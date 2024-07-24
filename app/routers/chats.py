from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Bubble
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
        #AI 답변 생성
        response_content = await bubble_service.create_bubble(db=db, chat_id=chat_id, content=req.content)

        response = StreamingResponse(bubble_service.create_bubble(db=db, chat_id=chat_id, content=req.content),
                                     media_type="text/event-stream")

        # AI 답변과 함께 매운맛 점수를 반환한다고 가정
        response_content = response['content']
        spicy_score = response['spicy_score']

        # Bubble 생성 및 저장
        bubble = Bubble(chat_id=chat_id, content=response_content, spicy_score=spicy_score)
        db.add(bubble)
        db.commit()

        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail="채팅하기에 실패했습니다.")

# 독한말 매운 맛 점수화
@router.get("/{chat_id}/spicy", response_model=ResultResponseModel, summary="채팅방 대화 내용의 매운 맛 점수 조회",
            description="채팅방의 대화 내용에 대한 매운 맛 점수를 조회합니다.")
def get_spicy_score(chat_id: int, db: Session = Depends(get_db)):
    bubbles = db.query(Bubble).filter(Bubble.chat_id == chat_id).all()
    if not bubbles:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")

    bubble_data = [{"content": bubble.content, "spicy_score": bubble.spicy_score} for bubble in bubbles]
    return ResultResponseModel(code=200, message="버블 리스트를 조회했습니다.", data=bubble_data)

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
