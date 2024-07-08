from pydantic import BaseModel
from datetime import datetime


class ImageBase(BaseModel):
    id : int
    bubble_id : int
    image_url: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
