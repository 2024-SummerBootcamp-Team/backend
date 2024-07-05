from pydantic import BaseModel
from typing import List

class ChatBubble(BaseModel):
    id: int
    writer: bool
    category: bool
    content: str
    created_at: str
    tts_count: int = 0
    image_count: int = 0

    class Config:
        orm_mode = True
