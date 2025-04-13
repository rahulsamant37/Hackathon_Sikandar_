from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.recommendation import Recommendation
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.ai.recommendation_service import get_recommendations_for_user

router = APIRouter()

@router.get("/recommendations", response_model=List[Recommendation])
def get_recommendations(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get personalized recommendations for the current user.
    """
    return get_recommendations_for_user(user_id=current_user.id)

@router.post("/analyze-learning-style")
def analyze_learning_style(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Analyze the user's learning style based on their activity.
    This is an asynchronous operation that will update the user's profile.
    """
    # This would trigger an async task to analyze the user's learning style
    return {"status": "analysis_started", "message": "Learning style analysis has been started"}
