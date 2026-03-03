from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import user as user_schemas
from app.services import users_service

router = APIRouter()


@router.post("/", response_model=user_schemas.UserRead)
def create_user(payload: user_schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = users_service.create_user(db, payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[user_schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return users_service.list_users(db)


@router.get("/{user_id}", response_model=user_schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
