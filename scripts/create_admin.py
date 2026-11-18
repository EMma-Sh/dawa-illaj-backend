"""Usage : python -m scripts.create_admin EMAIL PASSWORD FULL_NAME"""
import sys

from app.db import SessionLocal
from app.models import Role, User
from app.security import hash_password
from sqlalchemy import select

if len(sys.argv) != 4:
    sys.exit("Usage: python -m scripts.create_admin EMAIL PASSWORD FULL_NAME")

email , password , name = sys.argv[1], sys.argv[2] , sys.argv[3];

with SessionLocal() as db:
    if db.scalar(select(User).where(User.email == email.lower())):
        sys.exit("Is email ka user pehle se maujood hai.")
    db.add(
        User(
            email = email.lower(),
            password_hash = hash_password(password),
            full_name = name,
            role = Role.admin,
            is_approved = True,
        )
    )
    db.commit()
print("Admin created")