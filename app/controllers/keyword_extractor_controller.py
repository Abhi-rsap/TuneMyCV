from fastapi import APIRouter, HTTPException
from app.services.keyword_extraction_service import extract_keywords

router = APIRouter(prefix="/api/v1/keywords", tags=["Resume"])

@router.post("/resume", summary="Extract keywords from a job description")
async def extract_keywords_from_resume(job_description: str, company_name: str = None, role: str = None):
    try:
        return await extract_keywords(job_description, company_name, role)
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

