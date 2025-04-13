from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.user.preferences_service import (
    get_learning_style,
    get_notification_preferences,
    get_ui_preferences,
    get_user_preferences,
    update_learning_style,
    update_notification_preferences,
    update_ui_preferences,
    update_user_preferences
)

router = APIRouter()

class LearningStyleUpdate(BaseModel):
    primary_style: str = Field(..., description="Primary learning style (visual, auditory, reading, kinesthetic)")
    secondary_style: str = Field(None, description="Secondary learning style")
    pace_preference: str = Field(None, description="Pace preference (slow, moderate, fast)")

class NotificationPreferences(BaseModel):
    email: Dict = Field(..., description="Email notification preferences")
    in_app: Dict = Field(..., description="In-app notification preferences")

class UIPreferences(BaseModel):
    theme: str = Field(..., description="UI theme (light, dark)")
    font_size: str = Field(..., description="Font size (small, medium, large)")
    reduced_motion: bool = Field(..., description="Reduced motion preference")
    high_contrast: bool = Field(..., description="High contrast preference")

@router.get("/")
def read_preferences(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get all user preferences.
    """
    return get_user_preferences(user_id=current_user.id)

@router.put("/")
def update_preferences(
    preferences: Dict = Body(...),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Update user preferences.
    """
    success = update_user_preferences(user_id=current_user.id, preferences=preferences)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update preferences"
        )
    
    return get_user_preferences(user_id=current_user.id)

@router.get("/learning-style")
def read_learning_style(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get user's learning style preferences.
    """
    return get_learning_style(user_id=current_user.id)

@router.put("/learning-style")
def update_learning_style_preferences(
    style: LearningStyleUpdate,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Update user's learning style preferences.
    """
    success = update_learning_style(
        user_id=current_user.id,
        primary_style=style.primary_style,
        secondary_style=style.secondary_style,
        pace_preference=style.pace_preference
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update learning style preferences"
        )
    
    return get_learning_style(user_id=current_user.id)

@router.get("/notifications")
def read_notification_preferences(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get user's notification preferences.
    """
    return get_notification_preferences(user_id=current_user.id)

@router.put("/notifications")
def update_notification_prefs(
    prefs: NotificationPreferences,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Update user's notification preferences.
    """
    success = update_notification_preferences(
        user_id=current_user.id,
        notification_prefs=prefs.dict()
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification preferences"
        )
    
    return get_notification_preferences(user_id=current_user.id)

@router.get("/ui")
def read_ui_preferences(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get user's UI preferences.
    """
    return get_ui_preferences(user_id=current_user.id)

@router.put("/ui")
def update_ui_prefs(
    prefs: UIPreferences,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Update user's UI preferences.
    """
    success = update_ui_preferences(
        user_id=current_user.id,
        ui_prefs=prefs.dict()
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update UI preferences"
        )
    
    return get_ui_preferences(user_id=current_user.id)
