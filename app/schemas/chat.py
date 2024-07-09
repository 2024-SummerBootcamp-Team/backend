# schemas/chat_service.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ChatRoomBase(BaseModel):
    id: int
    character_id: int
    created_at: datetime
    name: str

    class Config:
        from_attributes = True

class ChatRoomBase(BaseModel):
    id: int
    character_id: int
    created_at: datetime
    name: str

    class Config:
        from_attributes = True


class ChatId(BaseModel):
    chat_id: int


class ChatCreateResponse(BaseModel):
    status_code: int
    message: str
    data: ChatId


class ChatCreateRequest(BaseModel):
    character_name: str = Field(..., min_length=1, max_length=45, title="캐릭터 이름")
    chat_name: str = Field(..., min_length=1, max_length=45, title="채팅방 이름")

