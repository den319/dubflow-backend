from app.models.user import User
from app.core.security import hash_password


def seed_users(db):
    user_defs = [
        {
            "email": "john@example.com",
            "username": "john",
            "password": "password123",
        },
        {
            "email": "alice@example.com",
            "username": "alice",
            "password": "password123",
        },
    ]

    users = []
    for ud in user_defs:
        u = db.query(User).filter(User.email == ud["email"]).first()
        if not u:
            u = User(
                email=ud["email"],
                username=ud["username"],
                hashed_password=hash_password(ud["password"]),
            )
            db.add(u)
        users.append(u)
    db.commit()

    return users