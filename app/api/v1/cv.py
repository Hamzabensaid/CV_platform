from fastapi import APIRouter, HTTPException, Body, status, Query
from pymongo import MongoClient
from bson import ObjectId, errors as bson_errors
from typing import List
from datetime import datetime

from app.models.cv_model import CV
from app.core.config import MONGO_URI, DB_NAME
from app.utils import sanitize_cv_data


router = APIRouter()

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["candidates"]

# Create unique index on email once at startup
collection.create_index("email", unique=True)
print("✅ Unique index created on email")


# Helper to convert MongoDB document to dict (removing _id)
def cv_helper(cv) -> dict:
    return {
        "id": str(cv["_id"]),
        "full_name": cv.get("full_name"),
        "email": cv.get("email"),
        "phone": cv.get("phone"),
        "location": cv.get("location"),
        "education": cv.get("education"),
        "experience": cv.get("experience"),
        "skills": cv.get("skills"),
        "languages": cv.get("languages"),
        "created_at": cv.get("created_at"),
        "updated_at": cv.get("updated_at"),
    }



@router.get("/", response_model=List[dict])
def get_all_cvs(
    full_name: str = Query(None),
    email: str = Query(None),
    location: str = Query(None),
    skill: str = Query(None),
    language: str = Query(None),
    education: str = Query(None),  # match degree or school
    experience: str = Query(None)  # match title or company
):
    filters = {}

    # Text search filters
    if full_name:
        filters["full_name"] = {"$regex": full_name, "$options": "i"}  # case-insensitive
    if email:
        filters["email"] = email
    if location:
        filters["location"] = {"$regex": location, "$options": "i"}

    # Array fields
    if skill:
        filters["skills"] = skill
    if language:
        filters["languages"] = language

    # Nested fields
    or_filters = []
    if education:
        or_filters.extend([
            {"education.degree": {"$regex": education, "$options": "i"}},
            {"education.school": {"$regex": education, "$options": "i"}}
        ])
    if experience:
        or_filters.extend([
            {"experience.title": {"$regex": experience, "$options": "i"}},
            {"experience.company": {"$regex": experience, "$options": "i"}}
        ])

    if or_filters:
        filters["$or"] = or_filters

    # Fetch data
    cvs = [cv_helper(cv) for cv in collection.find(filters)]

    if not cvs:
        raise HTTPException(status_code=404, detail="No CVs found with given filters")
    return cvs



@router.get("/{cv_id}", response_model=CV)
def get_cv_by_id(cv_id: str):
    try:
        object_id = ObjectId(cv_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid CV ID format")

    cv = collection.find_one({"_id": object_id})
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv_helper(cv)


@router.post("/", response_model=dict)
def create_cv(cv_data: dict = Body(...)):
    cv_data = sanitize_cv_data(cv_data)
    cv_data["created_at"] = datetime.utcnow()
    cv_data["updated_at"] = datetime.utcnow()

    existing_cv = collection.find_one({"email": cv_data.get("email")})
    if existing_cv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A CV with this email already exists."
        )
    inserted = collection.insert_one(cv_data)
    new_cv = collection.find_one({"_id": inserted.inserted_id})
    return cv_helper(new_cv)


@router.put("/{cv_id}", response_model=dict)
def update_cv(cv_id: str, updated_data: dict = Body(...)):
    updated_data = sanitize_cv_data(updated_data)
    updated_data["updated_at"] = datetime.utcnow()

    try:
        object_id = ObjectId(cv_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid CV ID format")

    result = collection.update_one(
        {"_id": object_id},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="CV not found")

    updated_cv = collection.find_one({"_id": object_id})
    return cv_helper(updated_cv)


@router.delete("/{cv_id}", response_model=dict)
def delete_cv(cv_id: str):
    try:
        object_id = ObjectId(cv_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid CV ID format")

    deleted_cv = collection.find_one({"_id": object_id})
    if not deleted_cv:
        raise HTTPException(status_code=404, detail="CV not found")

    collection.delete_one({"_id": object_id})
    return {"message": "CV deleted successfully", "id": cv_id}
