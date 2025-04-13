"""
Service for managing user preferences.
"""

from typing import Dict, Optional
from uuid import UUID

from app.core.logging import logger
from app.services.db import get_supabase_client

def get_user_preferences(user_id: UUID) -> Dict:
    """
    Get a user's preferences.
    
    Args:
        user_id: User ID
        
    Returns:
        User preferences
    """
    try:
        supabase = get_supabase_client()
        
        # Get user from database
        response = supabase.table("users").select("learning_preferences").eq("user_id", str(user_id)).execute()
        
        if not response.data:
            return {}
        
        preferences = response.data[0].get("learning_preferences", {})
        return preferences
    except Exception as e:
        logger.error(f"Error getting user preferences: {str(e)}")
        return {}

def update_user_preferences(user_id: UUID, preferences: Dict) -> bool:
    """
    Update a user's preferences.
    
    Args:
        user_id: User ID
        preferences: User preferences
        
    Returns:
        True if successful, False otherwise
    """
    try:
        supabase = get_supabase_client()
        
        # Get current preferences
        current_preferences = get_user_preferences(user_id)
        
        # Merge with new preferences
        merged_preferences = {**current_preferences, **preferences}
        
        # Update user in database
        supabase.table("users").update({"learning_preferences": merged_preferences}).eq("user_id", str(user_id)).execute()
        
        return True
    except Exception as e:
        logger.error(f"Error updating user preferences: {str(e)}")
        return False

def get_learning_style(user_id: UUID) -> Dict:
    """
    Get a user's learning style preferences.
    
    Args:
        user_id: User ID
        
    Returns:
        Learning style preferences
    """
    preferences = get_user_preferences(user_id)
    
    learning_style = {
        "primary_style": preferences.get("primary_style", "visual"),
        "secondary_style": preferences.get("secondary_style", "reading"),
        "pace_preference": preferences.get("pace_preference", "moderate")
    }
    
    return learning_style

def update_learning_style(user_id: UUID, primary_style: str, secondary_style: Optional[str] = None, pace_preference: Optional[str] = None) -> bool:
    """
    Update a user's learning style preferences.
    
    Args:
        user_id: User ID
        primary_style: Primary learning style (visual, auditory, reading, kinesthetic)
        secondary_style: Secondary learning style (optional)
        pace_preference: Pace preference (slow, moderate, fast) (optional)
        
    Returns:
        True if successful, False otherwise
    """
    # Validate learning styles
    valid_styles = ["visual", "auditory", "reading", "kinesthetic"]
    valid_paces = ["slow", "moderate", "fast"]
    
    if primary_style not in valid_styles:
        logger.error(f"Invalid primary learning style: {primary_style}")
        return False
    
    if secondary_style and secondary_style not in valid_styles:
        logger.error(f"Invalid secondary learning style: {secondary_style}")
        return False
    
    if pace_preference and pace_preference not in valid_paces:
        logger.error(f"Invalid pace preference: {pace_preference}")
        return False
    
    # Build preferences
    preferences = {"primary_style": primary_style}
    
    if secondary_style:
        preferences["secondary_style"] = secondary_style
    
    if pace_preference:
        preferences["pace_preference"] = pace_preference
    
    # Update preferences
    return update_user_preferences(user_id, preferences)

def get_notification_preferences(user_id: UUID) -> Dict:
    """
    Get a user's notification preferences.
    
    Args:
        user_id: User ID
        
    Returns:
        Notification preferences
    """
    preferences = get_user_preferences(user_id)
    
    notification_prefs = preferences.get("notifications", {})
    
    # Set defaults if not present
    if not notification_prefs:
        notification_prefs = {
            "email": {
                "course_updates": True,
                "new_content": True,
                "quiz_reminders": True,
                "achievement_earned": True,
                "course_completed": True
            },
            "in_app": {
                "course_updates": True,
                "new_content": True,
                "quiz_reminders": True,
                "achievement_earned": True,
                "course_completed": True,
                "recommendations": True
            }
        }
    
    return notification_prefs

def update_notification_preferences(user_id: UUID, notification_prefs: Dict) -> bool:
    """
    Update a user's notification preferences.
    
    Args:
        user_id: User ID
        notification_prefs: Notification preferences
        
    Returns:
        True if successful, False otherwise
    """
    # Get current preferences
    preferences = get_user_preferences(user_id)
    
    # Update notification preferences
    preferences["notifications"] = notification_prefs
    
    # Update preferences
    return update_user_preferences(user_id, preferences)

def get_ui_preferences(user_id: UUID) -> Dict:
    """
    Get a user's UI preferences.
    
    Args:
        user_id: User ID
        
    Returns:
        UI preferences
    """
    preferences = get_user_preferences(user_id)
    
    ui_prefs = preferences.get("ui", {})
    
    # Set defaults if not present
    if not ui_prefs:
        ui_prefs = {
            "theme": "light",
            "font_size": "medium",
            "reduced_motion": False,
            "high_contrast": False
        }
    
    return ui_prefs

def update_ui_preferences(user_id: UUID, ui_prefs: Dict) -> bool:
    """
    Update a user's UI preferences.
    
    Args:
        user_id: User ID
        ui_prefs: UI preferences
        
    Returns:
        True if successful, False otherwise
    """
    # Get current preferences
    preferences = get_user_preferences(user_id)
    
    # Update UI preferences
    preferences["ui"] = ui_prefs
    
    # Update preferences
    return update_user_preferences(user_id, preferences)
