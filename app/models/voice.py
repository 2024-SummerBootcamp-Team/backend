from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from ..database.session import Base
from sqlalchemy.orm import relationship


class Voice(Base):
    __tablename__ = "voice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bubble_id = Column(Integer, ForeignKey('bubble.id'))
    is_deleted = Column(Boolean, default=False) #기본값이 안지워진것
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    content = Column(Text, nullable=False)
    audio_url = Column(String(500), nullable=False)
    v_count = Column(Integer, default=1,nullable=False)
    bubble = relationship("Bubble", back_populates="voices")

