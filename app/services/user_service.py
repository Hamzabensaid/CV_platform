from datetime import datetime
from bson import ObjectId
from passlib.context import CryptContext
from app.models.user_model import user_helper
from app.core.database import user_collection  # injected MongoDB collection

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash plain password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed"""
    return pwd_context.verify(plain_password, hashed_password)


# ---- CRUD operations ----

def create_user(user_data: dict) -> dict:
    """Create a new user with hashed password and default role"""
    user_data["password"] = hash_password(user_data["password"])
    user_data["created_at"] = datetime.utcnow()
    user_data["role"] = user_data.get("role", "candidate")  # default role

    result = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)


def get_user_by_email(email: str) -> dict | None:
    """Find a user by email"""
    return user_collection.find_one({"email": email})


def get_user(user_id: str) -> dict | None:
    """Find a user by MongoDB _id"""
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(user) if user else None


def list_users(skip: int = 0, limit: int = 10) -> list[dict]:
    users = user_collection.find().skip(skip).limit(limit)
    return [user_helper(u) for u in users]


def authenticate_user(email: str, password: str) -> dict | None:
    """Authenticate user by email and password"""
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user
