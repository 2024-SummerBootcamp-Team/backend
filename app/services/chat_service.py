from app.models.chat import Chat as ChatModel
from sqlalchemy.orm import Session
from app.models.voice import Voice as TTSModel
from app.models.image import Image as ImageModel
from app.schemas.bubble import ChatBubble,ChatBubbleList
from app.models.bubble import Bubble as BubbleModel
from typing import List


def get_chat_room(db: Session, chat_room_id: int):  # 클라이언트가 알고싶어하는 채팅방 id가 chat_room_id임
    return db.query(ChatModel).filter(ChatModel.id == chat_room_id,ChatModel.is_deleted == False).first()


def get_bubbles(db: Session, chat_id: int):  # 클라이언트가 알고싶어하는 채팅방 id가 chat_id임
    bubbles = db.query(BubbleModel).filter(BubbleModel.chat_id == chat_id).all()  # 특정방의 말풍선들정보를 가지고 옴

    bubble_list = []
    for bubble in bubbles:
        tts_count = db.query(TTSModel).filter(TTSModel.bubble_id == bubble.id).count()
        image_count = db.query(ImageModel).filter(ImageModel.bubble_id == bubble.id).count()

        bubble_form = ChatBubble(
            id=bubble.id,
            writer=bubble.writer,
            category=bubble.category,
            content=bubble.content,
            created_at=bubble.created_at,
            tts_count=tts_count,
            image_count=image_count,
        )
        bubble_list.append(bubble_form)

    # 특정방의 말풍선 정보 + TTs랑 이미지 값을 한번에 보여줘야함 그떄 알기위해선 bubbles를 반복문으로 돌면서 각 bubble의 아이디를 통해서tts와 이미지의 갯수를 조회해옴 bubbletts와 이미지의 외래키인 chatbubble_id 이
    return ChatBubbleList(bubbles=bubble_list)




