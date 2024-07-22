import app.config.envSetting # 환경 변수를 가져오기 위한 설정
from fastapi import FastAPI ,Request
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import logging

from .routers import api

# FastAPI를 실행하기 위해 인스턴스 생성

app = FastAPI(
    title="Brain Washer API",
    description="Brain Washer API",
    version="1.0.0",
    contact={
        "name": "Brain Washer",
        "url": "http://www.brain-washer.net",
    })

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청을 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 허용할 메서드들 설정
    allow_headers=["*"],  # 모든 헤더를 허용
)


# prometeus
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)



# 라우팅 설정
"""
라우트란?
- 클라이언트로부터 요청을 받았을 때, 해당 요청을 처리할 수 있는 함수를 매핑하는 것
"""
app.include_router(api.router)

watchfiles_logger = logging.getLogger('watchfiles')
watchfiles_logger.setLevel(logging.WARNING)


logging.basicConfig(
    filename='/app/logs/app.log',  # 로그 파일 이름
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format='%(asctime)s %(levelname)s %(name)s %(message)s'  # 로그 메시지 포맷

)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response