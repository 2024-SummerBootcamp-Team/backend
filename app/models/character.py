from sqlalchemy import Column, Integer, String,DateTime,Boolean,ForeignKey,Text
from ..database.session import Base
from sqlalchemy.orm import relationship

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    is_deleted = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    name = Column(String(20), nullable=False)
    prompt = Column(Text, nullable=False)

    chats = relationship("Chat", back_populates="character")