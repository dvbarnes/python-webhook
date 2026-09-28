"""
Tiny demo proving the migrated schema works end-to-end:
insert a couple of users, then query them back.

Run:  python main.py
"""
from app.database import SessionLocal
from app.models import User

def main():
    with SessionLocal() as session:
        # Insert (skip if already seeded, so re-running is idempotent)
        if not session.query(User).filter_by(email="ada@example.com").first():
            session.add_all([
                User(email="ada@example.com", name="Ada Lovelace"),
                User(email="alan@example.com", name="Alan Turing"),
            ])
            session.commit()

        # Query
        users = session.query(User).order_by(User.id).all()
        print(f"{len(users)} user(s) in the database:")
        for u in users:
            print(f"  [{u.id}] {u.name} <{u.email}> created_at={u.created_at}")

from fastapi import FastAPI, Request, status

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Acknowledge receipt quickly to prevent timeouts from the sender
    payload = await request.json()
    if not payload.get("email"):
        return None
    
    with SessionLocal() as session:
        # Insert (skip if already seeded, so re-running is idempotent)
        if not session.query(User).filter_by(email="ada@example.com").first():
            session.add_all([
                User(email="ada@example.com", name="Ada Lovelace"),
                User(email="alan@example.com", name="Alan Turing"),
            ])
            session.commit()
        if not session.query(User).filter_by(email=payload.get("email")).first():
            print(f"Creating new user with email={payload.get('email')} and name={payload.get('name')}")
            session.add_all([
                User(email=payload.get("email"), name=payload.get("name"))
            ])
            session.commit()
                    
        # Query
        users = session.query(User).order_by(User.id).all()
        print(f"{len(users)} user(s) in the database:")
        for u in users:
            print(f"  [{u.id}] {u.name} <{u.email}> created_at={u.created_at}")
    # Return the newly created or existing user
        user = session.query(User).filter_by(email=payload.get("email")).first()
        return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)