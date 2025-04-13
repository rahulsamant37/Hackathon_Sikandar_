from datetime import datetime
from typing import Any, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.content import Content, ContentCreate, ContentUpdate
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.content.content_service import create_content, get_content, get_content_by_module, update_content
from app.services.db import get_supabase_client

router = APIRouter()

@router.get("/module/{module_id}", response_model=List[Content])
def read_content_by_module(
    module_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve all content items for a specific module.
    """
    return get_content_by_module(module_id=module_id)

@router.post("/", response_model=Content)
def create_new_content(
    content_in: ContentCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new content item.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return create_content(content_in=content_in)

@router.get("/{content_id}", response_model=Content)
def read_content(
    content_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get content item by ID.
    """
    content = get_content(content_id=content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content

@router.put("/{content_id}", response_model=Content)
def update_content_endpoint(
    content_id: str,
    content_in: ContentUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a content item.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    content = get_content(content_id=content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return update_content(content_id=content_id, content_in=content_in)

@router.post("/{content_id}/complete")
def mark_content_complete(
    content_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Mark a content item as completed by the current user.
    """
    supabase = get_supabase_client()

    # Check if content exists
    content = get_content(content_id=content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check if progress record exists
    progress = supabase.table("user_progress").select("*").eq("user_id", str(current_user.id)).eq("content_id", content_id).execute()

    if progress.data:
        # Update existing progress
        supabase.table("user_progress").update({
            "status": "completed",
            "completion_percentage": 100,
            "last_accessed": datetime.utcnow().isoformat()
        }).eq("progress_id", progress.data[0]["progress_id"]).execute()
    else:
        # Create new progress record
        progress_id = str(uuid4())
        supabase.table("user_progress").insert({
            "progress_id": progress_id,
            "user_id": str(current_user.id),
            "content_id": content_id,
            "status": "completed",
            "completion_percentage": 100,
            "last_accessed": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }).execute()

    return {"status": "success", "message": "Content marked as completed"}
