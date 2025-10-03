from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime

# ---- DB helper (MongoDB representation)
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user.get("role", "candidate"),
        "created_at": user.get("created_at"),
    }


# ---- Pydantic models (for validation) ----

# Allowed roles
RoleType = Literal["admin", "recruiter", "candidate", "viewer"]

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: RoleType = "candidate"  # default role


class UserCreate(UserBase):
    password: str  # plain password (will be hashed)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


# ---- Optional: UserDB model (internal use, hashed password) ----
class UserDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime

    class Config:
        orm_mode = True
