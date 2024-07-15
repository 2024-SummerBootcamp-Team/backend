import app.config.envSetting # 환경 변수를 가져오기 위한 설정
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from .routers import api

# FastAPI를 실행하기 위해 인스턴스 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청을 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 허용할 메서드들 설정
    allow_headers=["*"],  # 모든 헤더를 허용
)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)




# 라우팅 설정
"""
라우트란?
- 클라이언트로부터 요청을 받았을 때, 해당 요청을 처리할 수 있는 함수를 매핑하는 것
"""
app.include_router(api.router)
