
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from src.auth.config import fastapi_users
from src.auth.config import auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.tasks.router import router as router_task
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend

@asynccontextmanager
async def lifespan(application: FastAPI):
  redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
  FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
  yield

app = FastAPI(
  title = "Trading App",
  lifespan=lifespan
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

app.include_router(router_operation)
app.include_router(router_task)