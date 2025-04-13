from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel
from uuid import UUID

class ContentBase(BaseModel):
    title: str
    type: str  # video, text, quiz, etc.
    content: Dict
    metadata: Dict = {}
    version: int = 1

class ContentCreate(ContentBase):
    module_id: UUID

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict] = None
    metadata: Optional[Dict] = None
    version: Optional[int] = None

class Content(ContentBase):
    content_id: UUID
    module_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
