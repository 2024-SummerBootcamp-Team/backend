from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from ..database.session import Base


class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    name = Column(String(20), nullable=False)
    prompt = Column(Text, nullable=False)
