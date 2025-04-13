"""
This module defines the database schema for Supabase.
These are not SQLAlchemy models, but rather Python representations of the Supabase tables.
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: UUID
    email: EmailStr
    username: str
    password_hash: str
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None
    learning_preferences: Dict = {}


class Course(BaseModel):
    course_id: UUID
    title: str
    description: Optional[str] = None
    instructor_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str = "draft"


class Module(BaseModel):
    module_id: UUID
    course_id: UUID
    title: str
    description: Optional[str] = None
    sequence_number: int
    status: str = "draft"
    created_at: datetime
    updated_at: Optional[datetime] = None


class ContentItem(BaseModel):
    content_id: UUID
    module_id: UUID
    title: str
    type: str  # video, text, quiz, etc.
    content: Dict  # JSON content data
    metadata: Dict  # JSON metadata
    version: int = 1
    created_at: datetime
    updated_at: Optional[datetime] = None


class Quiz(BaseModel):
    quiz_id: UUID
    content_id: UUID  # Links to a content item
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None  # in seconds
    passing_score: int = 70  # percentage
    created_at: datetime
    updated_at: Optional[datetime] = None


class Question(BaseModel):
    question_id: UUID
    quiz_id: UUID
    text: str
    type: str  # multiple-choice, true-false, etc.
    options: List[Dict]  # JSON array of options
    correct_answer: Dict  # JSON correct answer data
    points: int = 1
    created_at: datetime


class Enrollment(BaseModel):
    enrollment_id: UUID
    user_id: UUID
    course_id: UUID
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "active"


class UserProgress(BaseModel):
    progress_id: UUID
    user_id: UUID
    content_id: UUID
    status: str  # not_started, in_progress, completed
    completion_percentage: int = 0
    last_accessed: Optional[datetime] = None
    created_at: datetime


class QuizSubmission(BaseModel):
    submission_id: UUID
    user_id: UUID
    quiz_id: UUID
    score: float
    answers: List[Dict]  # JSON array of answers
    submitted_at: datetime
    time_taken: int  # in seconds


class Achievement(BaseModel):
    achievement_id: UUID
    user_id: UUID
    type: str
    metadata: Dict  # JSON metadata
    awarded_at: datetime


class AIRecommendation(BaseModel):
    recommendation_id: UUID
    user_id: UUID
    content_id: UUID
    recommendation_type: str
    reasoning: str
    created_at: datetime
    status: str = "pending"
