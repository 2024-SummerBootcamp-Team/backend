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


@router.get("/{chat_id}", response_model=ChatRoomBase)
def read_chat_room(chat_id: int, db: Session = Depends(get_db)):
    chat_room = crud.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")

    return chat_room

@router.get("/{chat_id}/bubbles", response_model=ChatBubbleList)
def read_chat_bubble(chat_id: int, db: Session = Depends(get_db)):
    chat_room = crud.get_chat_room(db, chat_room_id=chat_id)
    if not chat_room:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    chat_bubble = crud.get_bubbles(db, chat_id=chat_id)


    return chat_bubble


