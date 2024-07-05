from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.session import Base

class TTS(Base):
    __tablename__ = "voice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chatbubble_id = Column(Integer, ForeignKey('chatBubble.id'))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    audio_url = Column(String(500), nullable=False)

    # bubble = relationship("ChatBubble", back_populates="ttss")

