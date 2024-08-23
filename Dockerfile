ARG PYTHON_IMG=python:3.12.5-slim-bookworm
ARG POETRY_VERSION=1.8.3

FROM ${PYTHON_IMG} as base

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code" \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=${POETRY_VERSION}

# Install necessary soft
RUN apt-get update \
    && apt-get install -y netcat-traditional curl git make gcc postgresql python3-dev libpq-dev \
    && apt-get clean
 # System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock /code/
COPY fastapi_postgres /code/fastapi_postgres/

FROM base as dev
# Project initialization:
RUN poetry install

COPY . /code/

CMD ["bash", "scripts/run.sh"]

FROM base as prod_builder

RUN poetry install --no-dev

FROM ${PYTHON_IMG} as prod

WORKDIR /code

COPY --from=prod_builder /code .

CMD ["bash", "scripts/run.sh"]
