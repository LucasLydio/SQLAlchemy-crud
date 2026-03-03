from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import profile as profile_schemas
from app.services import profiles_service

router = APIRouter()


@router.post("/", response_model=profile_schemas.ProfileRead)
def create_profile(payload: profile_schemas.ProfileCreate, db: Session = Depends(get_db)):
    try:
        profile = profiles_service.create_profile(db, payload)
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[profile_schemas.ProfileRead])
def list_profiles(db: Session = Depends(get_db)):
    return profiles_service.list_profiles(db)


@router.get("/{profile_id}", response_model=profile_schemas.ProfileRead)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = profiles_service.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
