from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.chat import ChatRoomBase
from ..services import chat_service
from ..database.session import get_db
from ..schemas.bubble import ChatBubbleList



router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{chat_id}", response_model=ChatRoomBase)
def read_chat_room(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")

    return chat_room

@router.get("/{chat_id}/bubbles", response_model=ChatBubbleList)
def read_chat_bubble(chat_id: int, db: Session = Depends(get_db)):
    chat_room = chat_service.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    chat_bubble = chat_service.get_bubbles(db, chat_id=chat_id)


    return chat_bubble


