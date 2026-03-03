from fastapi import FastAPI
from app.routes import users

app = FastAPI(title="SQLAlchemy CRUD - Users & Profiles")

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "API is running"}
