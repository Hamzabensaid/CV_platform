from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.cv_model import CVBase, CVCreateUpdate
from app.services.cv_service import (
    list_cvs,
    get_cv,
    create_cv,
    update_cv,
    delete_cv,
    get_top_skills,
    get_top_locations,
    get_education_distribution,
    get_experience_stats,
    match_candidates,
    count_cvs,
)

router = APIRouter()






# ---------------- Dashboard ----------------
@router.get("/dashboard")
def get_dashboard():
    try:
        total_cvs = count_cvs()  # ✅ fast count
        top_skills = get_top_skills(limit=5)
        top_locations = get_top_locations(limit=5)
        education_distribution = get_education_distribution()
        skills_distribution = get_top_skills(limit=50)
        experience_levels = get_experience_stats()
        recent = list_cvs({}, skip=0, limit=5, sort_by="created_at", sort_order=-1)

        return {
            "total_cvs": total_cvs,
            "recent": recent,
            "top_skills": top_skills,
            "top_locations": top_locations,
            "education_distribution": education_distribution,
            "skills_distribution": skills_distribution,
            "experience_levels": experience_levels,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")


# ---------------- Analytics ----------------
@router.get("/analytics/skills")
def analytics_skills(limit: int = 10):
    return get_top_skills(limit)


@router.get("/analytics/locations")
def analytics_locations(limit: int = 10):
    return get_top_locations(limit)


@router.get("/analytics/education")
def analytics_education():
    return get_education_distribution()


@router.get("/analytics/experience")
def analytics_experience():
    return get_experience_stats()


# ---------------- Candidate Matching ----------------
class JobDescription(BaseModel):
    skills: List[str]
    min_experience: int = 0
    top_n: int = 5


@router.post("/match")
def match_candidates_to_job(job: JobDescription):
    return match_candidates(job.skills, job.min_experience, job.top_n)


# ---------------- CV CRUD + Filters ----------------
@router.get("/", response_model=List[CVBase])
def get_all_cvs(
    search: str = Query(None),
    full_name: str = Query(None),
    email: str = Query(None),
    location: str = Query(None),
    skills: str = Query(None, description="Comma-separated skills"),
    skills_mode: str = Query("or", regex="^(and|or)$", description="Skill filter mode"),
    languages: str = Query(None, description="Comma-separated languages"),
    languages_mode: str = Query("or", regex="^(and|or)$", description="Language filter mode"),
    education: str = Query(None),
    experience: str = Query(None),
    min_experience_years: Optional[int] = Query(None, ge=0),
    max_experience_years: Optional[int] = Query(None, ge=0),
    created_from: Optional[str] = Query(None, description="Filter CVs created after this date (YYYY-MM-DD)"),
    created_to: Optional[str] = Query(None, description="Filter CVs created before this date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    filters = {}

    # Full-text search
    if search:
        filters["$text"] = {"$search": search}
    if full_name:
        filters["full_name"] = {"$regex": full_name, "$options": "i"}
    if email:
        filters["email"] = {"$regex": f"^{email}$", "$options": "i"}
    if location:
        filters["location"] = {"$regex": location, "$options": "i"}

    # ---- Skills filter
    if skills:
        skill_list = [s.strip() for s in skills.split(",")]
        if skills_mode == "and":
            filters["skills"] = {"$all": skill_list}
        else:
            filters["skills"] = {"$in": skill_list}

    # ---- Languages filter
    if languages:
        lang_list = [l.strip() for l in languages.split(",")]
        if languages_mode == "and":
            filters["languages"] = {"$all": lang_list}
        else:
            filters["languages"] = {"$in": lang_list}

    # ---- OR filters for nested fields
    or_filters = []
    if education:
        or_filters.extend([
            {"education.degree": {"$regex": education, "$options": "i"}},
            {"education.school": {"$regex": education, "$options": "i"}},
        ])
    if experience:
        or_filters.extend([
            {"experience.title": {"$regex": experience, "$options": "i"}},
            {"experience.company": {"$regex": experience, "$options": "i"}},
        ])
    if or_filters:
        filters["$or"] = or_filters

    # ---- Experience years range
    if min_experience_years or max_experience_years:
        exp_filter = {}
        if min_experience_years is not None:
            exp_filter["$gte"] = min_experience_years
        if max_experience_years is not None:
            exp_filter["$lte"] = max_experience_years
        filters["experience.years"] = exp_filter

    # ---- Date range
    date_filter = {}
    if created_from:
        try:
            date_filter["$gte"] = datetime.strptime(created_from, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid created_from format. Use YYYY-MM-DD.")
    if created_to:
        try:
            date_filter["$lte"] = datetime.strptime(created_to, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid created_to format. Use YYYY-MM-DD.")
    if date_filter:
        filters["created_at"] = date_filter

    # Sorting
    sort_order = -1 if order.lower() == "desc" else 1
    cvs = list_cvs(filters, skip, limit, sort_by, sort_order, search=bool(search))

    return cvs


@router.get("/{cv_id}", response_model=CVBase)
def get_cv_by_id(cv_id: str):
    cv = get_cv(cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv


@router.post("/", response_model=CVBase)
def create_cv_route(cv_data: CVCreateUpdate):
    return create_cv(cv_data)


@router.put("/{cv_id}", response_model=CVBase)
def update_cv_route(cv_id: str, updated_data: CVCreateUpdate):
    updated = update_cv(cv_id, updated_data)
    if not updated:
        raise HTTPException(status_code=404, detail="CV not found")
    return updated


@router.delete("/{cv_id}", response_model=dict)
def delete_cv_route(cv_id: str):
    deleted = delete_cv(cv_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="CV not found")
    return deleted
