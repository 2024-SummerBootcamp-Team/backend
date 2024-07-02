from fastapi import FastAPI
from .routers import api

# FastAPI를 실행하기 위해 인스턴스 생성
app = FastAPI()

# 라우팅 설정
"""
라우트란?
- 클라이언트로부터 요청을 받았을 때, 해당 요청을 처리할 수 있는 함수를 매핑하는 것
"""
app.include_router(api.router)
