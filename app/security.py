from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .config import settings

_ph = PasswordHasher()
# Email na milne par bhi login mein barabar time lage (user enumeration se bachao)
_DUMMY_HASH = _ph.hash("dummy-password")


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    try:
        ok = _ph.verify(password_hash or _DUMMY_HASH, password)
    except VerifyMismatchError:
        return False
    return ok and password_hash is not None


def create_access_token(user_id: int, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "role": role, "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])