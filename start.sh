alembic revision --autogenerate -m "describe the change" #creates the migration script
alembic upgrade head #migrates the database to the latest schema
uvicorn main:app --reload #runs the app