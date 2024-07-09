from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from ..schemas.chat import ChatRoomBase
from ..services import chat_service
from ..database.session import get_db
from ..schemas.bubble import ChatBubbleList
from ..schemas.chat import ChatCreateResponse, ChatCreateRequest, ChatId
from ..services import character_service

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




@router.post("", response_model=ChatCreateResponse)
def create_chat_room(req: ChatCreateRequest, db: Session = Depends(get_db)):
    vaild_character_name = character_service.validate_character_name(db, character_name=req.character_name)

    if not vaild_character_name:
        raise HTTPException(status_code=404, detail="캐릭터 이름 정보를 찾을 수 없습니다.")

    character_id = character_service.get_character_id_by_name(db,
                                                              character_name=req.character_name
                                                              )

    db_chat = chat_service.create_chat_room(db,
                                            chat_name=req.chat_name,
                                            character_id=character_id
                                            )

    if not db_chat:
        raise HTTPException(status_code=404, detail="채팅방 생성에 실패했습니다.")

    return ChatCreateResponse(status_code=200,
                              message="채팅방을 생성했습니다.",
                              data=ChatId(chat_id=db_chat.id)
                              )
