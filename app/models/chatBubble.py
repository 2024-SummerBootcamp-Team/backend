
from sqlalchemy import Column, Integer,DateTime,Boolean,Text,ForeignKey
from ..database.session import Base
from sqlalchemy.orm import relationship

class ChatBubble(Base):
    __tablename__ = "chatBubble"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    writer = Column(Boolean, nullable=False)  # AI (0) or User (1)
    category = Column(Boolean, nullable=False)  # Image (0) or Text (1)
    content = Column(Text, nullable=False)

    ttss= relationship("TTS", back_populates="bubble")
    chat= relationship("Chat", back_populates="bubbles")
    images= relationship("Image", back_populates="bubble")