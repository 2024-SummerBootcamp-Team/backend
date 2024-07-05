from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.session import Base

class TTS(Base):
    __tablename__ = "TTS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_bubble_id = Column(Integer, ForeignKey('chat_bubble.id'), nullable=False)
    audio_url = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False, nullable=False)

    bubble= relationship("ChatBubble", back_populates="ttss")

