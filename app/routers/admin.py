from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import require_role
from ..models import Role, User
from ..schemas import UserOut

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role(Role.admin))],  # poora router sirf admin ke liye
)


@router.get("/doctors/pending", response_model=list[UserOut])
def pending_doctors(db: Session = Depends(get_db)):
    q = select(User).where(User.role == Role.doctor, User.is_approved.is_(False))
    return db.scalars(q).all()


@router.post("/doctors/{user_id}/approve", response_model=UserOut)
def approve_doctor(user_id: int, db: Session = Depends(get_db)):
    doc = db.get(User, user_id)
    if not doc or doc.role != Role.doctor:
        raise HTTPException(404, "Doctor not found")
    doc.is_approved = True
    db.commit()
    return doc