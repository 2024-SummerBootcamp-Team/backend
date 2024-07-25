from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class ChatRoomBase(BaseModel):
    id: int
    character_id: int
    character_name: str
    topic: Optional[str] = None
    spicy: Optional[int] = None
    created_at: datetime
    name: str

    class Config:
        from_attributes = True

class ChatRoomCreateRequest(BaseModel):
    character_name: str = Field(..., min_length=1, max_length=45, title="캐릭터 이름")
    chat_room_name: str = Field(..., min_length=1, max_length=45, title="채팅방 이름")

