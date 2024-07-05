
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services import chat_room as crud
from ..database.session import get_db
from ..schemas import chat_rooms as schemas

router = APIRouter(
    prefix="/chats",
    tags=["chat_bubbles"],
    responses={404: {"description": "Not found"}},
)
@router.get("/bubbles/{bubbleId}", response_model=schemas.ChatBubble)
def read_chat_bubble(bubbleId: int, db: Session = Depends(get_db)):
    chat_bubble = crud.get_chat_bubble(db, bubble_id=bubbleId)
    if not chat_bubble:
        raise HTTPException(status_code=404, detail="버블 번호 찾을 수 없다")

    return chat_bubble
