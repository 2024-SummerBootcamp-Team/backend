
from sqlalchemy.orm import Session
from ..models.chat import ChatRoom as ChatRoomModel
from ..models.chat import ChatRoom as ChatModel


def get_chat_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ChatRoomModel).offset(skip).limit(limit).all()
#db: Session: SQLAlchemy의 세션 객체로, 데이터베이스와의 상호작용을 위한 인자입니다.
#skip: int = 0: 가져오기 시작할 데이터의 인덱스를 설정합니다.
#limit: int = 100: 최대로 가져올 데이터의 개수를 설정합니다.
#return: 지정된 범위의 채팅방 데이터를 리스트로 반환합니다
def get_chat_room(db: Session, room_id: int):
    return db.query(ChatRoomModel).filter(ChatRoomModel.id == room_id).first()
def get_chat(db: Session, bubble_id: int):
    return db.query(ChatRoomModel).filter(ChatModel.id == bubble_id).first()

