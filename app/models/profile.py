from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    profile_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Profile id={self.id} name={self.profile_name}>"
