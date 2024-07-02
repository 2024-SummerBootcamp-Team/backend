# 스키마 구조 정의이며 pydantic을 사용하여 스키마를 정의한다.
# 정의된 스키마는 API의 요청하는 값이나 응답하는 값의 형식을 정의한다.
# 해당 과정을 통해 API의 요청과 응답의 형식을 명확하게 정의할 수 있으며,
# 데이터 구조에 영향

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):

    class Config:
        from_attributes = True
