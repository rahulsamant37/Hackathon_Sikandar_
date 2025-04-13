from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.analytics.analytics_service import get_course_analytics, get_user_progress
from app.services.analytics.user_analytics_service import user_analytics
from app.services.analytics.content_analytics_service import content_analytics

router = APIRouter()

@router.get("/user-progress")
def read_user_progress(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the current user's progress across all courses.
    """
    return get_user_progress(user_id=current_user.id)

@router.get("/course/{course_id}")
def read_course_analytics(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get analytics for a specific course.
    Only available to instructors of the course or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return get_course_analytics(course_id=course_id)

@router.get("/user-activity")
def read_user_activity(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the current user's activity over a period of time.
    """
    return user_analytics.get_user_activity(user_id=current_user.id, days=days)

@router.get("/popular-content")
def read_popular_content(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the most popular content based on user activity.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user_analytics.get_popular_content(days=days, limit=limit)

@router.get("/user-retention")
def read_user_retention(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Calculate user retention over a period of time.
    Only available to admins.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user_analytics.get_user_retention(days=days)

@router.get("/content-engagement/{content_id}")
def read_content_engagement(
    content_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get engagement metrics for a specific content item.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return content_analytics.get_content_engagement(content_id=content_id)

@router.get("/course-engagement/{course_id}")
def read_course_engagement(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get engagement metrics for a course.
    Only available to instructors of the course or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return content_analytics.get_course_engagement(course_id=course_id)

@router.get("/content-difficulty/{content_id}")
def read_content_difficulty(
    content_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Analyze the difficulty of a content item based on user performance.
    Only available to instructors or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return content_analytics.get_content_difficulty_analysis(content_id=content_id)
