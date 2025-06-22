from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.document_parser_service import handle_document_upload
from app.services.resume_tailoring_service import resume_tailor_with_llm

router = APIRouter(prefix="/api/v1/tailor", tags=["Tailoring"])

@router.post("/resume", summary="Tailor a resume to match a job description")
async def tailor_resume(resume_file_name: str, job_description: str, company_name: str = None, role: str = None):
    try:
        return await resume_tailor_with_llm(resume_file_name, job_description, company_name, role)
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

