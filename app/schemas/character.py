from pydantic import BaseModel
from datetime import datetime
from typing import List

class CharacterDetail(BaseModel):
    id: int
    name: str
    image_url: str

    class Config:
        from_attributes = True

class CharacterList(BaseModel):
    characters: List[CharacterDetail]

    class Config:
        from_attributes = True