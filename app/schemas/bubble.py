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
