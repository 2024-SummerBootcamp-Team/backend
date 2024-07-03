# routers/chat_rooms.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services import chat_room as crud
from ..database.session import get_db
from ..schemas import chat_rooms as schemas

router = APIRouter(
    prefix="/chat",
    tags=["chat_rooms"],
    responses={404: {"description": "Not found"}},
)


@router.get("/room/{roomId}", response_model=schemas.ChatRoomBase)
def read_chat_room(roomId: int, db: Session = Depends(get_db)):
    chat_room = crud.get_chat_room(db, room_id=roomId)
    if chat_room is None:
        raise HTTPException(status_code=404, detail="Chat room not found")
    response = {
        "code": 200,
        "message": "채팅방 전체 내용을 조회했습니다.",
        "data": [{
            "id": "number",
            "writer": "string",
            "category": "string",
            "content": "string",
            "created_at": "string",
            "tts_count": 0,
            "image_count": 0
        }]

    }  # 단일 채팅방이므로 리스트에 담아서 반환
    return response

@router.get("/bubble/{bubble_id}", response_model=schemas.ChatRoomBase)
def read_chat_bubble(bubble_id: int, db: Session = Depends(get_db)):
    db_chat_bubble = crud.get_chat(db, bubble_id=bubble_id)
    if db_chat_bubble is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat_bubble
