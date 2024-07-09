from typing import List

from pydantic import BaseModel, Field
from datetime import datetime


class ImageBase(BaseModel):
    id : int
    bubble_id : int
    image_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ImageBaseList(BaseModel):
    images: List[ImageBase]

    class Config:
        from_attributes = True


class ImageDetail(BaseModel):
    id: int
    chat_id: int
    character: str
    bubble_id: int
    image_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ImageDetailList(BaseModel):
    images: List[ImageDetail]

    class Config:
        from_attributes = True

#발췌 이미지 생성
class ImageRoomBase(BaseModel):
    id: int
    bubble_id: int
    image_url: str
    content: str
    created_at: datetime

    class config:
        from_attributes = True

class ImageCreateRequest(BaseModel):
    content: str