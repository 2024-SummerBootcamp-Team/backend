# 서비스 폴더 보통 비즈니스 로직을 처리하는 파일이다.
# 비즈니스 로직이란, 사용자가 요청한 데이터를 처리하는 로직을 말한다.
from sqlalchemy.orm import Session
from ..models.user import User as UserModel
from ..schemas.users import User as UserSchema


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(UserModel).filter(UserModel.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSchema):
    db_user = UserModel(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
