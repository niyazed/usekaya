
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

from src.config.settings import settings
from src.db.models import CampaignModel, AdGroupModel, AdGroupStatsModel


engine = create_engine(url=settings.DATABASE_URL, 
                        echo=True, 
                        )
def init_db() -> None:
    """Creates all database tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Creates a new session for the database."""
    with Session(engine) as session:
        yield session
    




