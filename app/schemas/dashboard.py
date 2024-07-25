from typing import List
from pydantic import BaseModel, HttpUrl, Field


# 전체 캐릭터 통계

class TopicFrequency(BaseModel):
    취업: int = Field(alias="취업")
    학업: int = Field(alias="학업")
    인간관계: int = Field(alias="인간관계")
    연애: int = Field(alias="연애")

class SpicyFrequency(BaseModel):
    level_0_20: int = Field(alias="0-20")
    level_20_40: int = Field(alias="20-40")
    level_40_60: int = Field(alias="40-60")
    level_60_80: int = Field(alias="60-80")
    level_80_100: int = Field(alias="80-100")

    class Config:
        populate_by_name = True # 필드 이름을 기준으로 값을 채움

class CharacterStats(BaseModel):
    name: str
    chat_count: int
    topic_frequency: TopicFrequency
    spicy_frequency: SpicyFrequency

class DashboardTotal(BaseModel):
    characters: List[CharacterStats]


# 캐릭터 별 통계
class CharacterInfo(BaseModel):
    id: int
    name: str
    description: str

class ImageInfo(BaseModel):
    id: int
    url: str
    download: int

class VoiceInfo(BaseModel):
    id: int
    content: str
    url: str
    download: int

class DashboardCharacter(BaseModel):
    info: CharacterInfo
    top_images: List[ImageInfo]
    top_voices: List[VoiceInfo]
    topic_frequency: TopicFrequency
    average_spice_level: float
