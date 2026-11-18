from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
    role: Literal["patient", "doctor"] = "patient"  # admin signup se nahi banta
    pmdc_number: str | None = Field(default=None, max_length=30)
    specialty: str | None = Field(default=None, max_length=80)

    @model_validator(mode="after")
    def doctor_needs_pmdc(self):
        if self.role == "doctor" and not (self.pmdc_number or "").strip():
            raise ValueError("PMDC number is required for doctors")
        return self


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: str
    is_approved: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PendingDoctorOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    pmdc_number: str
    specialty: str | None