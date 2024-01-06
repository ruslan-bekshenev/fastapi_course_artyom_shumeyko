
from fastapi import Depends, FastAPI
from src.auth.config import fastapi_users
from src.auth.config import auth_backend, current_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
  title = "Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"