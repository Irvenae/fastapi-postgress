from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from fastapi_postgres.app import app
from fastapi_postgres.config import settings
from fastapi_postgres.database.models import Base
from fastapi_postgres.database.session import get_db_session


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    db_name = settings.database_url.split('/')[-1]
    db_url = settings.database_url.replace(f'/{db_name}', '/test')

    # Assume we run from localhost.
    server_string = settings.database_url.split('@')[-1]
    server_address = server_string.split(':')[0]
    db_url = db_url.replace(f'@{server_address}', '@localhost')

    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=test_app, base_url='http://test') as client:
        yield client
