from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from app.core.config import MONGO_URI, DB_NAME
from app.models.cv_model import CVCreateUpdate
from app.init import sanitize_cv_data

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["candidates"]

# Create indexes at startup
collection.create_index("email", unique=True)
collection.create_index([
    ("full_name", "text"),
    ("email", "text"),
    ("location", "text"),
    ("education.degree", "text"),
    ("education.school", "text"),
    ("experience.title", "text"),
    ("experience.company", "text"),
    ("skills", "text"),
    ("languages", "text")
])

# --------------------------
# Helper to convert MongoDB document to dict
# --------------------------
def cv_helper(cv) -> dict:
    return {
        "id": str(cv["_id"]),  # automatic id
        "full_name": cv.get("full_name"),
        "email": cv.get("email"),
        "phone": cv.get("phone"),
        "location": cv.get("location"),
        "education": cv.get("education", []),
        "experience": cv.get("experience", []),
        "skills": cv.get("skills", []),
        "languages": cv.get("languages", []),
        "created_at": cv.get("created_at"),
        "updated_at": cv.get("updated_at"),
    }

# --------------------------
# Service functions (CRUD + Search)
# --------------------------
def list_cvs(
    filters: Dict[str, Any],
    skip: int,
    limit: int,
    sort_by: str,
    sort_order: int,
    search: bool = False,
    search_query: Optional[str] = None,
    search_fields: Optional[List[str]] = None
):
    query: Dict[str, Any] = filters.copy()

    # Full-text or field-specific search
    if search_query:
        if search_fields:
            or_conditions = [
                {field: {"$regex": search_query, "$options": "i"}}
                for field in search_fields
            ]
            query["$or"] = or_conditions
        else:
            query["$text"] = {"$search": search_query}

    # Projection + sorting
    projection = {"score": {"$meta": "textScore"}} if search_query and not search_fields else None
    sort_fields = [("score", {"$meta": "textScore"})] if search_query and not search_fields else [(sort_by, sort_order)]

    cursor = (
        collection.find(query, projection)
        .sort(sort_fields)
        .skip(skip)
        .limit(limit)
    )
    return [cv_helper(cv) for cv in cursor]

def get_cv(cv_id: str) -> Optional[dict]:
    try:
        obj_id = ObjectId(cv_id)
    except:
        return None
    cv = collection.find_one({"_id": obj_id})
    return cv_helper(cv) if cv else None

def create_cv(cv_data: CVCreateUpdate) -> dict:
    cv_dict = sanitize_cv_data(cv_data.dict())
    cv_dict["created_at"] = datetime.utcnow()
    cv_dict["updated_at"] = datetime.utcnow()
    inserted = collection.insert_one(cv_dict)
    new_cv = collection.find_one({"_id": inserted.inserted_id})
    return cv_helper(new_cv)

def update_cv(cv_id: str, updated_data: CVCreateUpdate) -> Optional[dict]:
    try:
        obj_id = ObjectId(cv_id)
    except:
        return None
    updated_dict = sanitize_cv_data(updated_data.dict(exclude_unset=True))
    updated_dict["updated_at"] = datetime.utcnow()
    result = collection.update_one({"_id": obj_id}, {"$set": updated_dict})
    if result.matched_count == 0:
        return None
    updated_cv = collection.find_one({"_id": obj_id})
    return cv_helper(updated_cv)

def delete_cv(cv_id: str) -> Optional[dict]:
    try:
        obj_id = ObjectId(cv_id)
    except:
        return None
    cv = collection.find_one({"_id": obj_id})
    if not cv:
        return None
    collection.delete_one({"_id": obj_id})
    return {"message": "CV deleted successfully", "id": cv_id}

# --------------------------
# Analytics functions
# --------------------------
def get_top_skills(limit: int = 10):
    pipeline = [
        {"$unwind": "$skills"},
        {"$group": {"_id": "$skills", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    result = list(collection.aggregate(pipeline))
    return [{"skill": r["_id"], "count": r["count"]} for r in result]

def get_top_locations(limit: int = 10):
    pipeline = [
        {"$group": {"_id": "$location", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    result = list(collection.aggregate(pipeline))
    return [{"location": r["_id"], "count": r["count"]} for r in result if r["_id"]]

def get_education_distribution():
    pipeline = [
        {"$unwind": "$education"},
        {"$group": {"_id": "$education.degree", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    return [{"degree": r["_id"], "count": r["count"]} for r in result if r["_id"]]

def get_experience_stats():
    pipeline = [
        {"$unwind": "$experience"},
        {"$match": {"experience.years": {"$exists": True}}},
        {"$group": {
            "_id": None,
            "min_years": {"$min": "$experience.years"},
            "max_years": {"$max": "$experience.years"},
            "avg_years": {"$avg": "$experience.years"},
        }}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else {}

# --------------------------
# Candidate Matching
# --------------------------
def match_candidates(job_skills: List[str], min_experience: int = 0, top_n: int = 5):
    pipeline = [
        {
            "$addFields": {
                "skill_match_count": {"$size": {"$setIntersection": ["$skills", job_skills]}}
            }
        },
        {
            "$match": {
                "experience": {"$exists": True},
                # Optional: you may also want to filter by years of experience in nested experience list
            }
        },
        {
            "$sort": {"skill_match_count": -1}
        },
        {"$limit": top_n}
    ]
    results = list(collection.aggregate(pipeline))
    return [cv_helper(cv) for cv in results]  # map _id -> id

def count_cvs(filters: Dict[str, Any] = {}) -> int:
    """Return total number of CVs matching filters (fast count)."""
    return collection.count_documents(filters)