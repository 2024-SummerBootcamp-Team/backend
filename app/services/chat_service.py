from fastapi import HTTPException
from sqlalchemy import func

from app.models.chat import Chat
from sqlalchemy.orm import Session
from app.models.voice import Voice
from app.models.image import Image
from app.schemas.bubble import ChatBubble, ChatBubbleList
from app.schemas.chat import ChatRoomBase
from app.models.bubble import Bubble



# 채팅방 정보 조회
def get_chat_room(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.is_deleted == False).first()
    if not chat:
        raise HTTPException(status_code=404, detail="채팅방 정보를 불러오는데 실패했습니다.")
    return ChatRoomBase(
        id=chat.id,
        character_id=chat.character_id,
        character_name=chat.character.name,
        created_at=chat.created_at,
        name=chat.name
    )


# 전체 채팅 내용 조회
def get_bubbles(db: Session, chat_id: int,skip: int = 0, limit: int = 100):
    bubbles = db.query(Bubble).filter(Bubble.chat_id == chat_id).offset(skip).limit(limit).all()
    return ChatBubbleList(
        bubbles=[
            ChatBubble(
                id=bubble.id,
                writer=bubble.writer,
                category=bubble.category,
                content=bubble.content,
                created_at=bubble.created_at,
                tts_count=db.query(func.count(Voice.id)).filter(Voice.bubble_id == bubble.id).scalar(),
                image_count=db.query(func.count(Image.id)).filter(Image.bubble_id == bubble.id).scalar()
            )
            for bubble in bubbles
        ]
    )


# 채팅방 생성
def create_chat_room(db: Session, chat_name: str, character_id: int):
    chat = Chat(name=chat_name, character_id=character_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
