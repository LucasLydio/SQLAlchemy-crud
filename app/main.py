from fastapi import FastAPI
from app.api.routes import users as users_routes
from app.api.routes import profiles as profiles_routes

app = FastAPI(title="SQLAlchemy CRUD - Users & Profiles")

app.include_router(users_routes.router, prefix="/users", tags=["users"])
app.include_router(profiles_routes.router, prefix="/profiles", tags=["profiles"])


@app.get("/")
def root():
    return {"message": "API is running"}
