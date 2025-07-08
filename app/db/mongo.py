from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import pytz
from app.configs.config import timezone
import logging
from app.configs import config

client = AsyncIOMotorClient(config.mongo_db_url)
db = client.resume_bot
current_time_zone = pytz.timezone(timezone)

async def insert_document(collection_name: str, document: dict) -> dict:
    document['created_at'] = str(datetime.now(current_time_zone))
    collection = db[collection_name]

    result = await collection.insert_one(document)
    if not result.acknowledged:
        logging.error(f"Failed to insert document into '{collection_name}'")
        raise Exception(f"Failed to insert into {collection_name}")
    
    document["_id"] = str(result.inserted_id)
    logging.info(f"Document inserted into '{collection_name}' with _id={document['_id']}")
    return document

async def get_document_by_field(collection_name: str, field: str, value: str) -> dict:
    collection = db[collection_name]
    return await collection.find_one({field: value})
