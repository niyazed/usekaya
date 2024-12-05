from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from src.routers import campaigns, performance
from src.db.database import init_db
from src.utils.logger import logger
from src.utils.rate_limiter import limiter
from src.config.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    logger.info("Initializing Redis...")
    redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Redis initialization complete")
    yield
    logger.info("Closing database connection...")


# Main FastAPI Application
app = FastAPI(lifespan=lifespan)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
@limiter.limit("5/minute")
def status(request: Request) -> dict:
    logger.info("Status endpoint called")
    return {"status": "ok"}


@app.head("/healthz")
def healthcheck() -> dict:
    logger.info("Healthcheck endpoint called")
    return {"status": "ok"}

# Include routers here
app.include_router(campaigns.router, prefix="/api/v1", tags=["campaigns"])
app.include_router(performance.router, prefix="/api/v1", tags=["performance"])
