# schemas/chat_rooms.py

from pydantic import BaseModel
from datetime import datetime

class ChatRoomBase(BaseModel):
    id: int
    category: str
    content: str
    created_at: datetime
    tts_count: int
    image_count: int

class ChatRoom(ChatRoomBase):
    id: int
    class Config:
        from_attributes = True


