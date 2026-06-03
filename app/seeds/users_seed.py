from app.models.user import User
from app.core.security import hash_password


def seed_users(db):
    users = [
        User(
            email="john@example.com",
            username="john",
            hashed_password=hash_password("password123"),
        ),
        User(
            email="alice@example.com",
            username="alice",
            hashed_password=hash_password("password123"),
        ),
    ]

    db.add_all(users)
    db.commit()

    return users