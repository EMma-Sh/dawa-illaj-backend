from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .deps import require_role
from .models import Role, User
from .routers import admin,auth

# Tables ab Alembic banata hai, yahan create_all nahi

app = FastAPI(title="DawaAlliaj API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(admin.router)

# Role check ki misaal
@app.get("/patient/dashboard", tags=["demo"])
def patient_dashboard(user: User = Depends(require_role(Role.patient))):
    return {"message": f"Welcome {user.full_name}"}


@app.get("/doctor/dashboard", tags=["demo"])
def doctor_dashboard(user: User = Depends(require_role(Role.doctor))):
    return {"message": f"Welcome Dr. {user.full_name}"}