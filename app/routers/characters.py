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


# 대시보드
@router.get("/dashboard/total", response_model=ResultResponseModel, summary="전체 캐릭터 통계", description="전체 캐릭터에 대한 통계를 조회합니다.")
def read_dashboard_total(db: Session = Depends(get_db)):
    result = character_service.get_dashboard_total(db)
    return ResultResponseModel(code=200, message="전체 캐릭터에 대한 통계를 조회했습니다.", data=result)


@router.get("/dashboard/{character_name}", response_model=ResultResponseModel, summary="캐릭터 별 통계", description="캐릭터 별 통계를 조회합니다.")
def read_dashboard_character(character_name: str, db: Session = Depends(get_db)):
    result = character_service.get_dashboard_character(db, character_name)
    return ResultResponseModel(code=200, message="캐릭터에 대한 통계를 조회했습니다.", data=result)
