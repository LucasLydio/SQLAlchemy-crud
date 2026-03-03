from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app import services, schemas

router = APIRouter()

@router.post("/", response_model=schemas.user.UserRead)
def create_user(payload: schemas.user.UserCreate, db: Session = Depends(get_db)):
    # uniqueness is enforced by DB; services should raise on error
    try:
        user = services.user_service.create_user(db, payload)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.user.UserRead])
def list_users(db: Session = Depends(get_db)):
    return services.user_service.list_users(db)

@router.get("/{user_id}", response_model=schemas.user.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = services.user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
