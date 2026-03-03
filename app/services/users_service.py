from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, Profile
from app.schemas.user import UserCreate
from app.core.security import hash_password


def create_user(db: Session, user_in: UserCreate):
    profile_id = None
    if user_in.profile:
        profile = Profile(profile_name=user_in.profile.profile_name)
        db.add(profile)
        db.flush()
        profile_id = profile.id

    hashed = hash_password(user_in.password)
    user = User(name=user_in.name, email=user_in.email, password=hashed, profile_id=profile_id)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Email already in use")
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
