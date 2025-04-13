from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    sequence_number: int
    status: str = "draft"

class ModuleCreate(ModuleBase):
    course_id: UUID

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sequence_number: Optional[int] = None
    status: Optional[str] = None

class Module(ModuleBase):
    module_id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
