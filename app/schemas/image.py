from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageBase(BaseModel):
    image_url: str
    content: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    chat_bubble_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ImageResponse(BaseModel):
    code: int
    message: str
    data: Optional[Image]