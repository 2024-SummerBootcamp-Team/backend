from pydantic import BaseModel
from typing import Any, Optional


class ResultResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[Any]