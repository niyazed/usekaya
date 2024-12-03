from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routers import campaigns, performance
from src.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    yield
    print("Closing database connection...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def status() -> dict:
    return {"status": "ok"}

app.include_router(campaigns.router, prefix="/api/v1", tags=["campaigns"])
app.include_router(performance.router, prefix="/api/v1", tags=["performance"])
