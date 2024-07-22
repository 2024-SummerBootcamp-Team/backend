from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.chat import Chat

router = APIRouter(
    prefix="/healthcheck",
    tags=["health"]
)


class HealthCheck(BaseModel):
    status: str


@router.get("",
            response_model=HealthCheck,
            status_code=status.HTTP_200_OK,
            summary="Health Check",
            description="DB 연결 상태와 서버 상태를 확인합니다.")
async def health_check(db: Session = Depends(get_db)):
    test_query = db.query(Chat).first()

    if test_query:
        return HealthCheck(status="ok")
    else:
        return HealthCheck(status="fail")




