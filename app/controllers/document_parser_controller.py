from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.document_parser_service import handle_document_upload

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

@router.post("/upload", summary="Upload and parse a resume (Word document)")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only .docx and .doc files are supported")

    try:
        file_data = await file.read()
        parsed_document = handle_document_upload(file_data, file.filename)
        return JSONResponse(content=parsed_document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
