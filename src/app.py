from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.routers import campaigns, performance
from src.db.database import init_db
from src.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    yield
    logger.info("Closing database connection...")

app = FastAPI(lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def status() -> dict:
    logger.info("Status endpoint called")
    return {"status": "ok"}

# Include routers here
app.include_router(campaigns.router, prefix="/api/v1", tags=["campaigns"])
app.include_router(performance.router, prefix="/api/v1", tags=["performance"])
