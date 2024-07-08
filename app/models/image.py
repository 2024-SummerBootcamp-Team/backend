from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from ..database.session import Base
from sqlalchemy.orm import relationship


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bubble_id = Column(Integer, ForeignKey('bubble.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)

    bubble = relationship("Bubble", back_populates="images")
