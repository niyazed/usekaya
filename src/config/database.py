from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine, Session, SQLModel
from typing import AsyncGenerator

from src.config.settings import settings


engine = create_engine(url=settings.DATABASE_URL, 
                        echo=True, 
                        )
def init_db() -> None:
    """Creates all database tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates a new session for the database."""
    async with AsyncSession(engine) as session:
        yield session
    




