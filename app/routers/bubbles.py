
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..schemas.bubble import ChatBubble
from ..services import bubble as crud

router = APIRouter(
    prefix="/chats",
    tags=["chat"], #
    responses={404: {"description": "Not found"}},
)
@router.get("/bubbles/{bubble_id}", response_model=ChatBubble)
def read_chat_bubble(bubble_Id: int, db: Session = Depends(get_db)):
    chat_bubble = crud.get_bubbles(db, chat_id=bubble_Id)
    if not chat_bubble:
        raise HTTPException(status_code=404, detail="버블 번호 찾을 수 없다")

    return chat_bubble
