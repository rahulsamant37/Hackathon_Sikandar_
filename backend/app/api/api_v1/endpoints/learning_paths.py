from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.ai.learning_path_service import generate_learning_path

router = APIRouter()

@router.get("/{course_id}")
def get_learning_path(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Generate a personalized learning path for the current user in a specific course.
    """
    learning_path = generate_learning_path(user_id=current_user.id, course_id=course_id)
    
    if "error" in learning_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=learning_path["error"]
        )
    
    return learning_path
