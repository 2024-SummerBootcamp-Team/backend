from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import users as usersSchema
from ..services import user as crud
from ..database import session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[usersSchema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    return db_users


@router.post("", response_model=usersSchema.User)
def create_user(user: usersSchema.User, db: Session = Depends(session.get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    return crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=usersSchema.User)
def read_user(user_id: int, db: Session = Depends(session.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
