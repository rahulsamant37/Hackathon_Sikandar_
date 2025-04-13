from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "draft"

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    title: Optional[str] = None
    
class Course(CourseBase):
    id: UUID
    instructor_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
