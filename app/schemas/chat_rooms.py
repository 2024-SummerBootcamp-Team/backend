# schemas/chat_rooms.py

from pydantic import BaseModel
from datetime import datetime

class ChatRoomBase(BaseModel):
    writer: str
    category: str
    content: str
    createdAt: datetime
    tts: int
    image: int

class ChatRoom(ChatRoomBase):
    id: int

    class Config:
        orm_mode = True

class ChatRoomResponse(BaseModel):
    code: int
    message: str
    data: list[ChatRoom]
