import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import get_db
from .models import Role, User
from .security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    err = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    try:
        user_id = int(decode_token(token)["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise err
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise err
    return user  # role hamesha DB se, token ke role par bharosa nahi


def require_role(*roles: Role):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed for your role")
        if user.role == Role.doctor and not user.is_approved:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Doctor account pending approval")
        return user

    return checker