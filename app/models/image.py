from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from app.database import Base
from datetime import datetime

class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, index=True)
    bubble_id = Column(Integer, ForeignKey('chatbubble.id'), nullable=False)
    image_url = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

