import uuid
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_postgres.api import models
from fastapi_postgres.database import models as db_models
from fastapi_postgres.database.session import get_db_session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(prefix='/v1', tags=['v1'])


@router.post('/ingredients', status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    data: models.IngredientPayload,
    session: DBSessionDep,
) -> models.Ingredient:
    ingredient = db_models.Ingredient(**data.model_dump())
    session.add(ingredient)
    await session.commit()
    await session.refresh(ingredient)
    return models.Ingredient.model_validate(ingredient)


@router.get('/ingredients', status_code=status.HTTP_200_OK)
async def get_ingredients(session: DBSessionDep,) -> list[models.Ingredient]:
    ingredients = await session.scalars(select(db_models.Ingredient))
    return [models.Ingredient.model_validate(ingredient) for ingredient in ingredients]


@router.get('/ingredients/{pk}', status_code=status.HTTP_200_OK)
async def get_ingredient(
    pk: uuid.UUID,
    session: DBSessionDep,
) -> models.Ingredient:
    ingredient = await session.get(db_models.Ingredient, pk)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ingredient does not exist',
        )
    return models.Ingredient.model_validate(ingredient)


@router.post('/potions', status_code=status.HTTP_201_CREATED)
async def create_potion(
    data: models.PotionPayload,
    session: DBSessionDep,
) -> models.Potion:
    data_dict = data.model_dump()
    ingredients = await session.scalars(
        select(db_models.Ingredient).where(db_models.Ingredient.pk.in_(
            data_dict.pop('ingredients'))))
    potion = db_models.Potion(**data_dict, ingredients=list(ingredients))
    session.add(potion)
    await session.commit()
    await session.refresh(potion)
    return models.Potion.model_validate(potion)


@router.get('/potions', status_code=status.HTTP_200_OK)
async def get_potions(session: DBSessionDep,) -> list[models.Potion]:
    potions = await session.scalars(select(db_models.Potion))
    return [models.Potion.model_validate(potion) for potion in potions]


@router.get('/potions/{pk}', status_code=status.HTTP_200_OK)
async def get_potion(
    pk: uuid.UUID,
    session: DBSessionDep,
) -> models.Potion:
    potion = await session.get(db_models.Potion, pk)
    if potion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Potion does not exist',
        )
    return models.Potion.model_validate(potion)
