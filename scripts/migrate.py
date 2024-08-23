import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from fastapi_postgres.config import settings
from fastapi_postgres.database.models import Base

logger = logging.getLogger()


async def migrate_tables() -> None:
    logger.info('Starting to migrate')

    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info('Done migrating')


if __name__ == '__main__':
    asyncio.run(migrate_tables())
