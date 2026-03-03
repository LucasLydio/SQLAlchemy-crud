from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import hash_password

def create_user(db: Session, user_in: schemas.user.UserCreate):
    # create profile first if provided
    profile_id = None
    if user_in.profile:
        profile = models.profile.Profile(profile_name=user_in.profile.profile_name)
        db.add(profile)
        db.flush()
        profile_id = profile.id

    hashed = hash_password(user_in.password)
    user = models.user.User(name=user_in.name, email=user_in.email, password=hashed, profile_id=profile_id or None)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user.User).offset(skip).limit(limit).all()
