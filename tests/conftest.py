import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.app import app
from src.config.settings import settings

@pytest.fixture(autouse=True)
async def initialize_cache():
    redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    FastAPICache._cache = None  # Clear cache after tests

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
