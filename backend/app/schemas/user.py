from typing import Dict, Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str = "student"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    learning_preferences: Optional[Dict] = None
    
    class Config:
        from_attributes = True
