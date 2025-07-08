from app.db.mongo import insert_document, get_document_by_field
from app.utils.llm import extract_keywords_from_jd, tailor_resume_from_jd
import logging
from pydantic import ValidationError
async def resume_tailor_with_llm(resume_file_name: str, job_description: str, company_name: str = None, role: str = None) -> dict:
    # Step 0: Fetch base resume from DB
    resume_object = await get_document_by_field("documents", "filename", resume_file_name)
    if not resume_object:
        raise ValueError(f"No resume found with filename: {resume_file_name}")

    logging.info("✅ Resume fetched successfully from MongoDB.")

    # Step 1: Extract skills from the job description
    keywords = await extract_keywords_from_jd(job_description, model_name="llama3")
    logging.info(f"✅ Extracted keywords: {keywords}")

    # Step 2: Generate summary using skills and experience from resume
    updated_resume_json = await tailor_resume_from_jd(keywords, job_description,resume_object["content"])
    logging.info(f"✅ Generated summary: {updated_resume_json['summary']}")
    
    # Step 4: Store tailored resume
    tailored_document = {
        **updated_resume_json,
        "base_resume_id": str(resume_object["_id"]),
        "job_description": job_description,
        "company_name": company_name,
        "Role": role
    }

    try:
        return await insert_document("tailored_documents", tailored_document)
    except ValidationError as e:
        logging.error("❌ Tailored resume did not match the expected structure.")
        raise e
