"""
Integration test for handle_webhook in app/webhook_v2.py.

Uses a real Postgres database (kept separate from dev/prod via
TEST_DATABASE_URL) and drives the endpoint through FastAPI's
TestClient, which runs actual request/response handling -- this
is closer to a real HTTP call than mocking the DB session.
"""
import os

from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, SessionLocal
from main import app

load_dotenv()
TEST_DB_URL = os.environ.get("DATABASE_URL")
engine = create_engine(TEST_DB_URL)
TestSession = SessionLocal

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Fresh schema before every test so tests don't leak state into each other."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    

def test_webhook_seeds_and_returns_existing_user():
    response = client.post("/webhook", json={"email": "ada@example.com", "name": "Nobody"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "ada@example.com"
    assert body["name"] == "Ada Lovelace"


def test_webhook_seeds_both_users_even_if_only_one_requested():
    client.post("/webhook", json={"email": "ada@example.com", "name": "Nobody"})

    with TestSession() as session:
        from app.models import User
        emails = {u.email for u in session.query(User).all()}
    assert emails == {"ada@example.com", "alan@example.com"}


def test_webhook_unknown_email_creates_email():
    response = client.post("/webhook", json={"email": "nobody@example.com", "name": "Nobody"})

    assert response.status_code == 200
    with TestSession() as session:
        from app.models import User
        count = session.query(User).filter_by(email="nobody@example.com").count()
    assert count == 1


def test_webhook_missing_email_key_in_payload():
    response = client.post("/webhook", json={})

    assert response.status_code == 200
    assert response.json() is None


def test_webhook_called_twice_does_not_duplicate_seed_users():
    client.post("/webhook", json={"email": "ada@example.com"})
    client.post("/webhook", json={"email": "ada@example.com"})

    with TestSession() as session:
        from app.models import User
        count = session.query(User).filter_by(email="ada@example.com").count()
    assert count == 1