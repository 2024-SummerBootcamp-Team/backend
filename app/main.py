from fastapi import FastAPI
from .routers import api

app = FastAPI()

# 라우팅 설정
app.include_router(api.router)


