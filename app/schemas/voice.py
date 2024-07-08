from pydantic import BaseModel
from datetime import datetime

class VoiceBase(BaseModel):
    id: int
    bubble_id: int
    audio_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

