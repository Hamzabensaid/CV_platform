from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.user_service import get_user_by_email, verify_password
from app.models.user_model import UserOut

# Secret & algorithm
SECRET_KEY = "super-secret-key"  # TODO: move to env var
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme (must match login endpoint!)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# ---- Token utils ----
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ---- Auth helpers ----
def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password"]):
        return None
    return user


# ---- Dependency: get current user ----
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    role: str = payload.get("role", "candidate")  # read role from token
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut(**{
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "role": role,  # use role from token
        "created_at": user["created_at"],
    })
