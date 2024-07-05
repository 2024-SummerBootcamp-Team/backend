from pydantic import BaseModel
from datetime import datetime
class ChatBubble(BaseModel):
    id: int
    writer: bool
    category: bool
    content: str
    created_at: datetime
    tts_count: int = 0
    image_count: int = 0
    class Config:
        from_attributes = True