from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class Recommendation(BaseModel):
    id: UUID
    user_id: UUID
    content_id: UUID
    recommendation_type: str
    reasoning: str
    created_at: datetime
    status: str = "pending"
    
    class Config:
        from_attributes = True
