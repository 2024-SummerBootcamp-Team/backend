from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):

    class Config:
        from_attributes = True
