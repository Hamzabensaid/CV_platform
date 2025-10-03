from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re

# --------------------------
# Submodels
# --------------------------
class Education(BaseModel):
    degree: Optional[str] = None
    school: Optional[str] = None
    year: Optional[str] = None

    @field_validator('year')
    def year_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v.isdigit() or not (1900 <= int(v) <= 2100)):
            raise ValueError("Year must be a valid 4-digit number")
        return v

class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    technologies: Optional[List[str]] = []

# --------------------------
# Base model (used for DB responses)
# --------------------------
class CVBase(BaseModel):
    id: Optional[str] = Field(alias="_id")
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[List[Education]] = []
    experience: Optional[List[Experience]] = []
    skills: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }

# --------------------------
# Model for creating/updating (frontend form)
# --------------------------
class CVCreateUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[List[Education]] = []
    experience: Optional[List[Experience]] = []
    skills: Optional[List[str]] = []
    languages: Optional[List[str]] = []

    @field_validator('phone')
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        pattern = r'^\+?\d[\d\s\-x()]{7,20}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator('skills', 'languages')
    def validate_each_list(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return v
        for item in v:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("Skill or language cannot be empty")
        return v

# --------------------------
# Model for blank CV (for /new route)
# --------------------------
