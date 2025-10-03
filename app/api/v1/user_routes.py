from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user_model import UserCreate, UserOut
from app.services.user_service import create_user, get_user_by_email, list_users, authenticate_user
from app.core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

router = APIRouter(tags=["Users"])

# ---- Register
@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate):
    existing = get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(user_data.dict())
    return user

# ---- Login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)  # username = email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user["email"], "role": user.get("role", "candidate")},
        expires_delta=access_token_expires,
    )
    return {"access_token": token, "token_type": "bearer"}

# ---- Current user
@router.get("/me", response_model=UserOut)
def get_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user

# ---- List users (open to all)
@router.get("/", response_model=list[UserOut])
def get_users(skip: int = Query(0), limit: int = Query(10)):
    """
    List users (no role required)
    """
    return list_users(skip=skip, limit=limit)