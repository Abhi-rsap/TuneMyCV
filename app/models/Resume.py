from typing import Optional
from pydantic import BaseModel

class Resume(BaseModel):
    header: str
    summary: Optional[str]
    education: str
    skills: str
    experience: str
    projects: Optional[str]