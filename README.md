# Alembic + SQLAlchemy MVP (Postgres)

Minimal working example of database change management for a greenfield Python project, targeting Postgres.

## Setup

1. Have a Postgres instance running and a database created:
   ```bash
   createdb app_dev
   ```
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your connection string (or rely on the default, which matches a local
   `postgres`/`postgres`/`localhost:5432`/`app_dev` setup):
   ```bash
   cp .env.example .env
   export $(cat .env | xargs)   # or use python-dotenv / your framework's env loading
   ```

## Run migrations
```bash
alembic upgrade head
```

## Try it
```bash
python main.py
```
Inserts two users, then prints them back out. Safe to re-run (idempotent seed).

## Making a schema change
1. Edit/add a model in `app/models.py` (must inherit from `Base` in `app/database.py`)
2. Generate a migration:
   ```bash
   alembic revision --autogenerate -m "describe your change"
   ```
3. **Review the generated file in `alembic/versions/`** — autogenerate is good but not perfect (renamed columns show as drop+add, some constraints get missed, data migrations aren't generated at all).
4. Apply it:
   ```bash
   alembic upgrade head
   ```

## Rolling back
```bash
alembic downgrade -1        # back one migration
alembic history             # see the full chain
```

## Switching environments (dev/staging/prod)
Both `main.py` and `alembic/env.py` read `DATABASE_URL` from the environment
(via `app/database.py`), so pointing at a different Postgres instance is just
an env var change — no code edits needed:
```bash
DATABASE_URL=postgresql+psycopg://user:pass@prod-host:5432/mydb alembic upgrade head
```

## What's included
- `app/database.py` — engine, session factory, declarative Base; reads `DATABASE_URL` from env
- `app/models.py` — two related models (`User`, `Post`) to show a foreign key
- `alembic/` — migration environment, wired to autogenerate off `app.models` and to use the same `DATABASE_URL` as the app
- `alembic/versions/` — initial migration creating both tables
- `main.py` — smoke test script
- `.env.example` — connection string template
