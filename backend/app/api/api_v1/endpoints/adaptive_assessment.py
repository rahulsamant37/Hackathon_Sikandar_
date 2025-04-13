from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.ai.adaptive_assessment_service import (
    create_adaptive_assessment,
    evaluate_adaptive_assessment
)

router = APIRouter()

class AnswerSubmission(BaseModel):
    question_id: str
    answer_data: Dict

class AssessmentSubmission(BaseModel):
    assessment_id: str
    answers: List[AnswerSubmission]

@router.post("/create/{course_id}")
def create_assessment(
    course_id: str,
    num_questions: int = 10,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Create an adaptive assessment for a course.
    """
    if num_questions < 5 or num_questions > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of questions must be between 5 and 30"
        )
    
    assessment = create_adaptive_assessment(current_user.id, course_id, num_questions)
    
    if "error" in assessment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=assessment["error"]
        )
    
    return assessment

@router.post("/submit")
def submit_assessment(
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Submit an adaptive assessment.
    """
    if not submission.answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No answers provided"
        )
    
    # Convert pydantic models to dictionaries
    answers = [
        {
            "question_id": answer.question_id,
            "answer_data": answer.answer_data
        }
        for answer in submission.answers
    ]
    
    result = evaluate_adaptive_assessment(current_user.id, submission.assessment_id, answers)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result
