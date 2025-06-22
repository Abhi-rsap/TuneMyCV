from app.models.Resume import Resume
from datetime import datetime
import pytz
from app.configs.config import timezone
import logging
from app.utils.llm import generate_response
from pydantic import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017/")

db = client.resume_bot
collection = db.tailored_documents
base_collection = db.documents
current_time_zone = pytz.timezone(timezone)


async def save_tailored_resume_to_db(tailored_resume_data: dict) -> dict:
    
    tailored_resume_data['created_at'] = str(datetime.now(current_time_zone))


    # Insert the document into the MongoDB collection
    result = await collection.insert_one(tailored_resume_data)
    tailored_resume_data["_id"] = str(result.inserted_id)
    if not result.acknowledged:
        logging.error("Failed to save tailored resume data to MongoDB.")
        raise Exception("Failed to save tailored resume data to MongoDB.")

    logging.info("Tailored resume data saved successfully to MongoDB.")
    return tailored_resume_data


async def resume_tailor_with_llm(resume_file_name: str, job_description: str,  company_name: str = None, role: str = None) -> dict:
    #Get json from MongoDB
    try:
        resume_object = await base_collection.find_one({"filename": resume_file_name})
        if not resume_object:
            raise ValueError(f"No resume found with filename: {resume_file_name}")
    except Exception as e:
        logging.error(f"Error fetching resume from MongoDB: {str(e)}")
        raise ValueError(f"Error fetching resume from MongoDB: {str(e)}")
    

    
    logging.info("Resume fetched successfully from MongoDB.")
    llm_response = await generate_response(resume_object['content'], job_description)

    if llm_response:
        try:
            llm_response['base_resume_id'] = str(resume_object['_id'])
            llm_response['job_description'] = job_description
            llm_response['company_name'] = company_name
            llm_response['Role'] = role
            
            saved_resume = await save_tailored_resume_to_db(llm_response)
            logging.info("Tailored resume saved successfully.")

            return saved_resume

        except ValidationError as e:
            print("❌ LLM response did not match the expected structure.")
            print(e)
    else:
        print("❌ Resume tailoring failed.")

