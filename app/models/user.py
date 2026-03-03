from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=True, unique=True)

    profile = relationship("Profile", backref="user", uselist=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
