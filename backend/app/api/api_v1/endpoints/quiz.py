from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.quiz import Quiz, QuizCreate, QuizSubmission, QuizSubmissionCreate, QuizUpdate
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.content.quiz_service import create_quiz, get_quiz, submit_quiz, update_quiz

router = APIRouter()

@router.post("/", response_model=Quiz)
def create_new_quiz(
    quiz_in: QuizCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new quiz.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return create_quiz(quiz_in=quiz_in)

@router.get("/{quiz_id}", response_model=Quiz)
def read_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get quiz by ID.
    """
    quiz = get_quiz(quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz

@router.put("/{quiz_id}", response_model=Quiz)
def update_quiz_endpoint(
    quiz_id: str,
    quiz_in: QuizUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a quiz.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    quiz = get_quiz(quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return update_quiz(quiz_id=quiz_id, quiz_in=quiz_in)

@router.post("/{quiz_id}/submit", response_model=QuizSubmission)
def submit_quiz_endpoint(
    quiz_id: str,
    submission: QuizSubmissionCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Submit a quiz.
    """
    if submission.quiz_id != quiz_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz ID in path and body do not match"
        )
    
    quiz = get_quiz(quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return submit_quiz(user_id=current_user.id, submission=submission)
