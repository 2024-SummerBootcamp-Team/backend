from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from ..database.session import Base
from sqlalchemy.orm import relationship


class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    name = Column(String(20), nullable=False)
    prompt = Column(Text, nullable=False)
    tts_id = Column(String(45), nullable=False)
    image_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    chats = relationship("Chat", back_populates="character")
