# schemas/chat_rooms.py

from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatRoomBase(BaseModel): #말풍선 딱 한개에 대한 정보
    id: int #말풍선마다의 번호
    writer : bool # ai가 말한 말풍선이냐 아님 내가 내가 말한 말풍선이냐
    category: bool #말풍선이 이미지형이냐 아님 텍스트형인지 판별
    content: str #말풍선 내용
    created_at: datetime #생성일자
    tts_count: int # 그 말풍선 하나당 tts를 몇 개 가지고 있나
    image_count: int # 그 말풍선 하나당 image를 몇 개 가지고 있냐
    character_id: int

class ChatRoomList(BaseModel): #채팅창 다 한꺼번에 보는 것
    data: List[ChatRoomBase] #ChatRoomBase애로 모든 말풍선정보를 받은걸 리스트로 담음


