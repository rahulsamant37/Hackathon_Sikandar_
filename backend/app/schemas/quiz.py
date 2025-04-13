from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID

class QuestionBase(BaseModel):
    text: str
    type: str  # multiple-choice, true-false, etc.
    options: List[Dict]
    correct_answer: Dict
    points: int = 1

class QuestionCreate(QuestionBase):
    quiz_id: UUID

class Question(QuestionBase):
    question_id: UUID
    quiz_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None  # in seconds
    passing_score: int = 70  # percentage

class QuizCreate(QuizBase):
    content_id: UUID
    questions: List[QuestionBase] = []

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    passing_score: Optional[int] = None

class Quiz(QuizBase):
    quiz_id: UUID
    content_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    questions: List[Question] = []
    
    class Config:
        from_attributes = True

class AnswerSubmission(BaseModel):
    question_id: UUID
    answer_data: Dict

class QuizSubmissionCreate(BaseModel):
    quiz_id: UUID
    answers: List[AnswerSubmission]
    time_taken: int  # in seconds

class QuizSubmission(BaseModel):
    submission_id: UUID
    user_id: UUID
    quiz_id: UUID
    score: float
    answers: List[Dict]
    submitted_at: datetime
    time_taken: int
    
    class Config:
        from_attributes = True
