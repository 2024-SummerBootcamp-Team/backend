from typing import List

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


class VoiceBaseList(BaseModel):
    voices: List[VoiceBase]

    class Config:
        from_attributes = True


class VoiceDetail(BaseModel):
    id: int
    chat_id: int
    character: str
    character_image: str
    bubble_id: int
    audio_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class VoiceDetailList(BaseModel):
    voices: List[VoiceDetail]

    class Config:
        from_attributes = True


# tts 생성 테스트
class VoiceCreateRequest(BaseModel):
    bubble_id: int
    content: str

    class Config:
        from_attributes = True
