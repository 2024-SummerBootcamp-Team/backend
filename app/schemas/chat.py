# schemas/chat.py

from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatRoomBase(BaseModel):
    id: int
    character_id: int
    created_at: datetime
    name: str

    class Config:
        from_attributes = True



