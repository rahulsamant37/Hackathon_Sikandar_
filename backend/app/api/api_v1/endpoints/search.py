from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.search_service import search_service

router = APIRouter()

@router.get("/courses")
def search_courses(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    instructor_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search for courses.
    """
    filters = {}
    if instructor_id:
        filters["instructor_id"] = instructor_id
    
    return search_service.search_courses(
        query=q,
        limit=limit,
        offset=offset,
        filters=filters
    )

@router.get("/content")
def search_content(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    module_id: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search for content.
    """
    filters = {}
    if module_id:
        filters["module_id"] = module_id
    
    if content_type:
        filters["type"] = content_type
    
    return search_service.search_content(
        query=q,
        limit=limit,
        offset=offset,
        filters=filters
    )

@router.get("/all")
def search_all(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Search for courses and content.
    """
    return search_service.search_all(
        query=q,
        limit=limit,
        offset=offset
    )
