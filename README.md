# fastapi-postgres

## First installation

In this project we are using Poetry, you can install it by

```
pipx install poetry
poetry config virtualenvs.in-project true # store virtualEnv in same folder as project.
```

If pipx is not found you can install it by (MacOS)

```
brew install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions in global scope.
```

Create the virtual environment by

```
poetry install --with-dev
```

Install pre-commit hooks by

```
pre-commit install -t pre-commit
```

## Usage

## Debugging

### Connect to database

Install psql

```
brew install libpq
brew link --force libpq
```

Try and connect to database running in docker-compose

```
psql -h 127.0.1 -p 5432 -U postgres
```

use

```
\l
```

to list the databases.

### Missing test database

If the test database is missing it is probably because you don't have the right
permissions on the startup script of the database

```
/usr/local/bin/docker-entrypoint.sh: /docker-entrypoint-initdb.d/create_test_db.sh: /bin/bash: bad interpreter: Permission denied
```

you need to change the permissions of the file and reinitialize the db

```
chmod +x ./scripts/create_test_db.sh
docker-compose rm
docker volume rm fastapi-sql_postgres_data
```

# Cannot connect to database

Generally you will encounter this error

```
socket.gaierror: [Errno 8] nodename nor servname provided, or not known
```

Make sure to check your `DATABASE_URL` environment variable. More in particular
make sure after the `@` you either use `localhost` or the docker-compose name
`postgres` (when connecting from there).
