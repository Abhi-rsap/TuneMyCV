from pymongo import MongoClient
from app.models.Resume import Resume
from app.utils.parse_resume import parse_resume
from datetime import datetime
import pytz
from app.configs.config import timezone
import logging
from io import BytesIO


client = MongoClient("mongodb://localhost:27017/")


db = client.resume_bot
collection = db.documents
current_time_zone = pytz.timezone(timezone)


def save_document_to_db(title: str, resume_data: Resume, filename: str) -> dict:
    
    resume_data_dict = resume_data.model_dump()
    doc_dict = {
        "title": title,
        "filename": filename,
        "content": resume_data_dict,
        "created_at": str(datetime.now(current_time_zone))
    }

    # Insert the document into the MongoDB collection
    result = collection.insert_one(doc_dict)
    doc_dict["_id"] = str(result.inserted_id)
    if not result.acknowledged:
        logging.error("Failed to save resume data to MongoDB.")
        raise Exception("Failed to save resume data to MongoDB.")

    logging.info("Resume data saved successfully to MongoDB.")


    return doc_dict

def handle_document_upload(file_data: bytes, filename: str) -> dict:
    f = BytesIO(file_data)
    parsed_data_json = parse_resume(f)
    #Validate and parse the JSON data into a Resume model
    if not parsed_data_json:
        raise ValueError("Failed to parse resume data from the document")
    try:
        # parsed_data_json = parsed_data_json.model_dump()
        resume_dict = Resume(**parsed_data_json)

        logging.info("Validated resume data successfully.")
        json_response = save_document_to_db(
            title= resume_dict.header.split("\n")[0] if resume_dict.header else "Resume",
            resume_data=resume_dict,
            filename=filename
        )


        return json_response
    except Exception as e:
        raise ValueError(f"Error validating parsed data: {str(e)}")

    
    # return save_document_to_db(resume_data.contact_information.full_name or "Untitled", resume_data, filename)

