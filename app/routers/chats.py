from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.chat import ChatRoomBase
from ..services import chat as crud #services 모듈에서 chat_room을 가져오고, 이를 crud로 이름을 변경하여 사용합니다. 이 모듈은 데이터베이스 작업(CRUD 작업)을 수행하는 함수들을 포함하고 있습니다
from ..database.session import get_db
from ..schemas.bubble import ChatBubbleList



router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{room_Id}", response_model=ChatRoomBase)
def read_chat_room(room_Id: int, db: Session = Depends(get_db)):
    chat_room = crud.get_chat_room(db, chat_room_id=room_Id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅 방 찾을 수 없다")

    return chat_room

@router.get("/bubbles/{bubble_Id}", response_model=ChatBubbleList)
def read_chat_bubble(bubble_Id: int, db: Session = Depends(get_db)):
    chat_bubble = crud.get_bubbles(db, chat_id=bubble_Id)
    if not chat_bubble:
        raise HTTPException(status_code=404, detail="버블 번호 찾을 수 없다")

    return chat_bubble


