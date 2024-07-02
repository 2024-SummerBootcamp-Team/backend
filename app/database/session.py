from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False
                  },
    pool_size=20,          # 기본 풀 크기
    max_overflow=40,       # 최대 오버플로우 수
    pool_timeout=30,       # 풀에서 커넥션을 가져오기 위해 대기하는 최대 시간(초)
    pool_recycle=1800,     # 연결을 재활용하기 전에 대기할 시간(초)
    pool_pre_ping=True     # 연결이 살아있는지 확인하기 위해 사전 핑을 활성화
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
