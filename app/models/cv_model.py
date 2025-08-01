from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime



class Education(BaseModel):
    degree: str
    school: str
    year: str

    @validator('year')
    def year_must_be_valid(cls, v):
        if not v.isdigit() or not (1900 <= int(v) <= 2100):
            raise ValueError("Year must be a valid 4-digit number")
        return v


class Experience(BaseModel):
    title: str
    company: str
    duration: str
    technologies: List[str]


class CV(BaseModel):
    id: Optional[str] = Field(alias="_id")  # Maps MongoDB's _id to id
    full_name: str
    email: EmailStr
    phone: str

    @validator('phone')
    def validate_phone(cls, v):
        pattern = r'^\+?\d[\d\s\-x()]{7,20}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v


    location: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    languages: List[str]

    @validator('skills', 'languages', each_item=True)
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Skill or language cannot be empty")
        return v
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
    
        populate_by_name = True  # Pydantic v2
        from_attributes = True   # Helps with parsing from MongoDB format
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            # Optional: add encoder for ObjectId if needed
        }
