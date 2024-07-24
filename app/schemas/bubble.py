from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatBubble(BaseModel):
    id: int
    writer: bool
    category: bool
    content: str
    created_at: datetime
    tts_count: int = 0
    image_count: int = 0

class ChatBubbleList(BaseModel):
    bubbles: List[ChatBubble]

    class Config:
        from_attributes = True

class BubbleRequest(BaseModel):
    content: str

    class Config:
        from_attributes = True

class BubbleRequest(BaseModel)
    content: str
    spicy_score: int # AI로부터 반환되는 spicy_score 필드 추가