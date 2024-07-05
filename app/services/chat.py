from sqlalchemy.orm import Session

from app.models.chat import Chat as ChatModel


def get_chat_room(db: Session, chat_room_id: int):  # 클라이언트가 알고싶어하는 채팅방 id가 chat_room_id임
    return db.query(ChatModel).filter(ChatModel.id == chat_room_id).first()



