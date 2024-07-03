from sqlalchemy import Column, Integer, String,DateTime,Boolean
from ..database.session import Base

class ChatRoom(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted=Column(Boolean, default=False)
