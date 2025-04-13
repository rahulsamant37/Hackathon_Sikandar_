from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.notification_service import notification_service

router = APIRouter()

@router.get("/")
def read_notifications(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """
    Get notifications for the current user.
    """
    return notification_service.get_user_notifications(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        unread_only=unread_only
    )

@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: str = Path(...),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Mark a notification as read.
    """
    success = notification_service.mark_notification_as_read(
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found or does not belong to user"
        )
    
    return {"status": "success"}

@router.put("/read-all")
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Mark all notifications as read.
    """
    success = notification_service.mark_all_notifications_as_read(
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark all notifications as read"
        )
    
    return {"status": "success"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: str = Path(...),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Delete a notification.
    """
    success = notification_service.delete_notification(
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found or does not belong to user"
        )
    
    return {"status": "success"}
