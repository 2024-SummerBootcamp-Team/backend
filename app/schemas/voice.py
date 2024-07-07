from typing import List

from pydantic import BaseModel
from datetime import datetime

class VoiceBase(BaseModel):
    id: int
    audio_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class VoiceList(BaseModel):
    voices: List[VoiceBase]

    class Config:
        from_attributes = True