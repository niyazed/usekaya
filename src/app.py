from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.routers import campaigns, performance
from src.db.database import init_db
from src.utils.logger import logger
from src.utils.rate_limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
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
