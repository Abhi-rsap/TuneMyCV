from app.db.mongo import insert_document
from app.utils.llm import extract_keywords_from_jd
import logging
from pydantic import ValidationError

async def extract_keywords(job_description: str, company_name: str = None, role: str = None) -> dict:
    
    # Step 1: Extract skills from the job description
    keywords = await extract_keywords_from_jd(job_description, model_name="llama3")
    logging.info(f"✅ Extracted keywords: {keywords}")
    
    # Step 2: Store keywords and job description in DB
    saved_document = {
        "keywords": keywords,
        "job_description": job_description,
        "company_name": company_name,
        "Role": role
    }

    try:
        return await insert_document("keywords_extraction", saved_document)
    except ValidationError as e:
        logging.error("❌ Keywords extraction did not match the expected structure.")
        raise e