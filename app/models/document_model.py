from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from app.models.resume_model import Resume

class Document(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    file_name: str
    content: Resume
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))

    class Config:
        validate_by_name = True
        json_encoders = \
        {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
        arbitrary_types_allowed = True

