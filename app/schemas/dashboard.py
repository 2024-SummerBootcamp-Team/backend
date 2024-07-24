from typing import List
from pydantic import BaseModel, HttpUrl, Field


# 전체 캐릭터 통계

class TopicFrequency(BaseModel):
    employment: int = Field(alias="취업")
    academics: int = Field(alias="학업")
    relationships: int = Field(alias="인간관계")
    romance: int = Field(alias="연애")

class Spicy(BaseModel):
    level_1_2: int = Field(alias="1-2")
    level_2_4: int = Field(alias="2-4")
    level_5_6: int = Field(alias="5-6")
    level_7_8: int = Field(alias="7-8")
    level_9_10: int = Field(alias="9-10")

class CharacterDetail(BaseModel):
    name: str
    topic_frequency: TopicFrequency
    spicy: Spicy

class DashboardTotal(BaseModel):
    characters: List[CharacterDetail]


# 캐릭터 별 통계
class CharacterInfo(BaseModel):
    id: int
    name: str
    description: str

class ImageInfo(BaseModel):
    id: int
    url: str

class VoiceInfo(BaseModel):
    id: int
    content: str
    url: str

class DashboardCharacter(BaseModel):
    info: CharacterInfo
    top_images: List[ImageInfo]
    top_voices: List[VoiceInfo]
    topic_frequency: TopicFrequency
    average_spice_level: float
