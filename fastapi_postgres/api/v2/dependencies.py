from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_postgres.database import models
from fastapi_postgres.database import repository
from fastapi_postgres.database import session

DBSessionDep = Annotated[AsyncSession, Depends(session.get_db_session)]


def get_repository(
    model: type[models.Base],) -> Callable[[AsyncSession], repository.DatabaseRepository]:

    def func(session: DBSessionDep):
        return repository.DatabaseRepository(model, session)

    return func
