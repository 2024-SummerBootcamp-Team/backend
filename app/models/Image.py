
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.session import Base

class Image(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_bubble_id = Column(Integer, ForeignKey('chat_bubble.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)

    bubble= relationship("ChatBubble", back_populates="images")