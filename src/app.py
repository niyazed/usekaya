from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.configs.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()
    yield
    print("Closing database connection...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def status() -> dict:
    return {"status": "ok"}