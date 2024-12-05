from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Request

from src.utils.logger import logger
from src.config.settings import settings
from src.db.models import CampaignModel, AdGroupModel, AdGroupStatsModel


engines = {
    'master': create_engine(settings.MASTER_DATABASE_URL,
                            logging_name='master'),
    'replica': create_engine(settings.REPLICA_DATABASE_URL,
                             logging_name='replica'),
}

async def init_db() -> None:
    """Creates all database tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engines['master'])


def get_session(request: Request):
    # Determine engine based on context (e.g., request method)
    engine = 'replica' if request.method == 'GET' else 'master'
    logger.info(f"Using {engine} engine, method: {request.method}")
    with Session(engines[engine]) as session:
        yield session




