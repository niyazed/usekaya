from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine, Session, SQLModel
from typing import AsyncGenerator

from src.configs.settings import settings

print(settings.DATABASE_URL)
engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

# async def init_db() -> None:
#     """Creates all database tables defined in SQLModel models."""
#     async with engine.connect() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

def init_db() -> None:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)

    SQLModel.metadata.create_all(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates a new session for the database."""
    async with AsyncSession(engine) as session:
        yield session
    




