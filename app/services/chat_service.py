from fastapi import HTTPException

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
                tts_count=db.query(Voice).filter(Voice.bubble_id == bubble.id).count(),
                image_count=db.query(Image).filter(Image.bubble_id == bubble.id).count()
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

def update_chat_spicy(db: Session, chat_id: int):
    # 최근 10개의 대화 버블을 불러옵니다.
    bubbles = db.query(Bubble).filter(Bubble.chat_id == chat_id).order_by(Bubble.created_at.desc()).limit(10).all()
    content = "\n\n".join(bubble.content for bubble in bubbles)

    # GPT에게 매운맛 지수 요청
    response = gpt_analyze_spiciness({"input": content})
    spicy_index = response.get("spiciness_index", 0)  # GPT 응답에서 매운맛 지수를 가져옴

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    chat.spicy_index = spicy_index
    db.commit()

    return spicy_index


def new_chat_message(db: Session, chat_id: int, message: str):
    # 새로운 메시지를 Bubble 테이블에 저장
    new_bubble = Bubble(chat_id=chat_id, content=message)
    db.add(new_bubble)
    db.commit()


def add_new_message(db: Session, chat_id: int, message: str):
    # 메시지를 추가하고 저장
    new_chat_message(db, chat_id, message)
    # 메시지 추가 후 매운맛 지수 업데이트
    update_chat_spicy(db, chat_id)


def calculate_spicy(db: Session, chat_id: int):
    # 요청 시 매운맛 지수를 계산하고 업데이트
    spicy_index = update_chat_spicy(db, chat_id)
    print("spicy_index", spicy_index)


def update_spicy_index(db: Session, chat_id: int):
    # 매운맛 지수 업데이트 요청
    calculate_spicy(db, chat_id)