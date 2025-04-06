from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    additional_links: Optional[Dict[str, str]] = None


class EducationEntry(BaseModel):
    institution_name: str
    degree: str
    field_of_study: str
    start_month: Optional[str] = None
    start_year: Optional[int] = None
    end_month: Optional[str] = None
    end_year: Optional[int] = None
    gpa: Optional[float] = None

class WorkExperienceEntry(BaseModel):
    job_title: str
    company_name: str
    start_month: Optional[str] = None
    start_year: Optional[int] = None
    end_month: Optional[str] = None
    end_year: Optional[int] = None
    description: List[str] = []


class Resume(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str] = None
    education: List[EducationEntry] = []
    work_experience: List[WorkExperienceEntry] = [] 
    skills: List[str] = []
    additonal_sections: Dict[str, dict] = {}