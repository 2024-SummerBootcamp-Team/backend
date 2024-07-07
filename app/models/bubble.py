
from sqlalchemy import Column, Integer,DateTime,Boolean,Text,ForeignKey
from ..database.session import Base


class ChatBubble(Base):
    __tablename__ = "bubble"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    writer = Column(Boolean, nullable=False,server_default="0")  # AI (0) or User (1)
    category = Column(Boolean, nullable=False,server_default="0")  # Image (0) or Text (1)
    content = Column(Text, nullable=False)
