from sqlalchemy.orm import Session
from app.models import Profile
from app.schemas.profile import ProfileCreate


def create_profile(db: Session, profile_in: ProfileCreate):
    profile = Profile(profile_name=profile_in.profile_name)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, profile_id: int):
    return db.query(Profile).filter(Profile.id == profile_id).first()


def list_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Profile).offset(skip).limit(limit).all()
