from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.character import CharacterList
from app.schemas.response import ResultResponseModel
from app.services import character_service

router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)


# 캐릭터 목록 조회
@router.get("", response_model=ResultResponseModel, summary="캐릭터 목록 조회", description="캐릭터 목록 및 정보를 조회합니다.")
def read_characters(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    characters = character_service.get_characters(db, skip=skip, limit=limit)
    return ResultResponseModel(code=200, message="캐릭터 목록을 조회했습니다.", data=CharacterList(characters=characters))
