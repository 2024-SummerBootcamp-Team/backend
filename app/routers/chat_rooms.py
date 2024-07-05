from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.chat_rooms import ChatRoomList
from ..services import chat_room as crud #services 모듈에서 chat_room을 가져오고, 이를 crud로 이름을 변경하여 사용합니다. 이 모듈은 데이터베이스 작업(CRUD 작업)을 수행하는 함수들을 포함하고 있습니다
from ..database.session import get_db
from ..schemas import chat_rooms as schemas


router = APIRouter(
    prefix="/chats",
    tags=["chat_rooms"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{room_id}", response_model=ChatRoomList)
def read_chat_room(room_id: int, db: Session = Depends(get_db)):
    chat_room = crud.get_chats(db, chat_id=room_id)
    # if not chat_room:
    #     raise HTTPException(status_code=404, detail="채팅 방 찾을 수 없다")

    return chat_room

