from fastapi import FastAPI

from fastapi_postgres.api.v1.routes import router as v1_router
from fastapi_postgres.api.v2.routes import router as v2_router
from fastapi_postgres.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
)

app.include_router(v1_router, prefix='/api')
app.include_router(v2_router, prefix='/api')
