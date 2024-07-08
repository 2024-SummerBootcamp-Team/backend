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
<<<<<<< HEAD

=======
class VoiceDeleted(BaseModel):
    id: int
    audio_url: str
    content: str
    created_at: datetime


    class Config:
        from_attributes = True
>>>>>>> 23b37cf49905fd1022efa82695360b12032d0747
