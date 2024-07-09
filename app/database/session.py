from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.config import get_settings
from ..config.aws.secret import get_secret
import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

"""
aws secret manager를 사용하여 데이터베이스 정보를 가져오는 방법

aws 시크릿으로 가져오는 이유는 보안상의 이유로 환경변수에 직접적으로 데이터베이스 정보를 넣지 않기 위함이다.
또한, aws 시크릿을 사용하면 데이터베이스 정보를 변경할 때 환경변수를 변경하지 않아도 되기 때문에 편리하다.
만약 키가 유출되었을 때는 aws에서 변경하면 됨으로 간단히 조치할 수 있다.
"""

"""
json.load 메소드는 문자열을 읽거나 파일을 읽고 파이썬 객체인 딕셔너리로 변환한다.
json 형태로 오는 aws 시크릿 데이터를 파싱하여 딕셔너리로 변환한다.
"""

secrets = json.loads(get_secret())

DATABASE_URL = secrets.get('DATABASE_URL')
DATABASE_USERNAME = secrets.get('DATABASE_USERNAME')
DATABASE_PASSWORD = secrets.get('DATABASE_PASSWORD')
DATABASE_PORT = secrets.get('DATABASE_PORT')
DATABASE_DBNAME = secrets.get('DATABASE_DBNAME')

# print(secrets)
#
# DATABASE_URL = get_settings().MYSQL_URL
# DATABASE_USERNAME = get_settings().MYSQL_USERNAME
# DATABASE_PASSWORD = get_settings().MYSQL_PASSWORD
# DATABASE_PORT = get_settings().MYSQL_PORT
# DATABASE_DBNAME = get_settings().MYSQL_DBNAME


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_DBNAME}'
#SQLALCHEMY_DATABASE_URL = 'sqlite:///.test.db'

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 10},

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
