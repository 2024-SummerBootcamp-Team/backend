from pydantic import BaseModel
from typing import List

class CharacterDetail(BaseModel):
    id: int
    name: str
    image_url: str
    description: str

    class Config:
        from_attributes = True

class CharacterList(BaseModel):
    characters: List[CharacterDetail]

    class Config:
        from_attributes = True
