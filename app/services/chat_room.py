
from sqlalchemy.orm import Session
from ..models.chat import ChatRoom as ChatRoomModel
from ..schemas.chat_rooms import ChatRoom as ChatRoomSchema

def get_chat_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ChatRoomModel).offset(skip).limit(limit).all()

def get_chat_room(db: Session, room_id: int):
    return db.query(ChatRoomModel).filter(ChatRoomModel.id == room_id).first()