from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.ai.content_generation_service import (
    generate_quiz_questions,
    generate_content_summary,
    generate_learning_objectives,
    generate_content_outline
)

router = APIRouter()

@router.post("/quiz-questions")
def create_quiz_questions(
    topic: str,
    difficulty: str,
    num_questions: int = 5,
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """
    Generate quiz questions for a given topic.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Difficulty must be one of: easy, medium, hard"
        )
    
    if num_questions < 1 or num_questions > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of questions must be between 1 and 20"
        )
    
    questions = generate_quiz_questions(topic, difficulty, num_questions)
    return questions

@router.post("/content-summary")
def create_content_summary(
    content_text: str,
    max_length: int = 500,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Generate a summary of educational content.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if not content_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content text is required"
        )
    
    if max_length < 100 or max_length > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Max length must be between 100 and 2000 characters"
        )
    
    summary = generate_content_summary(content_text, max_length)
    return {"summary": summary}

@router.post("/learning-objectives")
def create_learning_objectives(
    topic: str,
    difficulty: str,
    num_objectives: int = 5,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Generate learning objectives for a given topic.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if difficulty not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Difficulty must be one of: beginner, intermediate, advanced"
        )
    
    if num_objectives < 1 or num_objectives > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of objectives must be between 1 and 10"
        )
    
    objectives = generate_learning_objectives(topic, difficulty, num_objectives)
    return {"objectives": objectives}

@router.post("/content-outline")
def create_content_outline(
    topic: str,
    num_sections: int = 5,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Generate an outline for educational content.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if num_sections < 1 or num_sections > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of sections must be between 1 and 10"
        )
    
    outline = generate_content_outline(topic, num_sections)
    return outline
