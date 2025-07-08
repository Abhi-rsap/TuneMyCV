from app.models.Resume import Resume
from app.utils.parse_resume import parse_resume
from io import BytesIO
from app.db.mongo import insert_document
import logging

async def handle_document_upload(file_data: bytes, filename: str) -> dict:
    f = BytesIO(file_data)
    parsed_data_json = await parse_resume(f)
    
    if not parsed_data_json:
        raise ValueError("Failed to parse resume data from the document")

    try:
        resume_dict = Resume(**parsed_data_json)
        logging.info("Validated resume data successfully.")

        doc = {
            "title": resume_dict.header.split("\n")[0] if resume_dict.header else "Resume",
            "filename": filename,
            "content": resume_dict.model_dump()
        }

        return await insert_document("documents", doc)

    except Exception as e:
        raise ValueError(f"Error validating parsed data: {str(e)}")
