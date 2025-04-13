"""
Service for sending notifications to users.
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from app.core.logging import logger
from app.services.db import get_supabase_client
from app.services.email_service import email_service
from app.services.user.preferences_service import get_notification_preferences

class NotificationService:
    """
    Service for sending notifications to users.
    """
    
    def __init__(self):
        """
        Initialize the notification service.
        """
        self.supabase = get_supabase_client()
    
    def send_notification(
        self,
        user_id: UUID,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None,
        send_email: bool = False
    ) -> bool:
        """
        Send a notification to a user.
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional data (optional)
            send_email: Whether to send an email notification (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check user notification preferences
            preferences = get_notification_preferences(user_id)
            
            # Check if in-app notification is enabled for this type
            in_app_enabled = preferences.get("in_app", {}).get(notification_type, True)
            
            if in_app_enabled:
                # Create notification
                notification = {
                    "user_id": str(user_id),
                    "type": notification_type,
                    "title": title,
                    "message": message,
                    "data": data or {},
                    "read": False,
                    "created_at": datetime.utcnow().isoformat()
                }
                
                # Save notification to database
                self.supabase.table("notifications").insert(notification).execute()
            
            # Check if email notification is enabled for this type
            email_enabled = preferences.get("email", {}).get(notification_type, True)
            
            if send_email and email_enabled:
                # Get user email
                user_response = self.supabase.table("users").select("email, username").eq("user_id", str(user_id)).execute()
                
                if user_response.data:
                    user = user_response.data[0]
                    email = user["email"]
                    username = user["username"]
                    
                    # Send email notification
                    self._send_email_notification(
                        email=email,
                        username=username,
                        title=title,
                        message=message,
                        notification_type=notification_type
                    )
            
            return True
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return False
    
    def _send_email_notification(
        self,
        email: str,
        username: str,
        title: str,
        message: str,
        notification_type: str
    ) -> bool:
        """
        Send an email notification.
        
        Args:
            email: Recipient email
            username: Recipient username
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create email subject
            subject = f"{title} - AI Learning Platform"
            
            # Create email content
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4f46e5; color: white; padding: 10px 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>{title}</h1>
                    </div>
                    <div class="content">
                        <p>Hello {username},</p>
                        <p>{message}</p>
                        <p>Best regards,<br>The AI Learning Platform Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply to this message.</p>
                        <p>You received this email because you are subscribed to {notification_type} notifications. You can update your notification preferences in your account settings.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Hello {username},
            
            {message}
            
            Best regards,
            The AI Learning Platform Team
            
            This is an automated email. Please do not reply to this message.
            You received this email because you are subscribed to {notification_type} notifications. You can update your notification preferences in your account settings.
            """
            
            # Send email
            return email_service.send_email(
                to_email=email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False
    
    def get_user_notifications(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False
    ) -> List[Dict]:
        """
        Get notifications for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of notifications to return
            offset: Offset for pagination
            unread_only: Whether to return only unread notifications
            
        Returns:
            List of notifications
        """
        try:
            query = self.supabase.table("notifications").select("*").eq("user_id", str(user_id)).order("created_at", desc=True).limit(limit).offset(offset)
            
            if unread_only:
                query = query.eq("read", False)
            
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error getting user notifications: {str(e)}")
            return []
    
    def mark_notification_as_read(self, notification_id: str, user_id: UUID) -> bool:
        """
        Mark a notification as read.
        
        Args:
            notification_id: Notification ID
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if notification belongs to user
            notification_response = self.supabase.table("notifications").select("user_id").eq("id", notification_id).execute()
            
            if not notification_response.data:
                logger.error(f"Notification not found: {notification_id}")
                return False
            
            notification_user_id = notification_response.data[0]["user_id"]
            
            if notification_user_id != str(user_id):
                logger.error(f"Notification {notification_id} does not belong to user {user_id}")
                return False
            
            # Mark notification as read
            self.supabase.table("notifications").update({"read": True}).eq("id", notification_id).execute()
            
            return True
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            return False
    
    def mark_all_notifications_as_read(self, user_id: UUID) -> bool:
        """
        Mark all notifications for a user as read.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Mark all notifications as read
            self.supabase.table("notifications").update({"read": True}).eq("user_id", str(user_id)).eq("read", False).execute()
            
            return True
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {str(e)}")
            return False
    
    def delete_notification(self, notification_id: str, user_id: UUID) -> bool:
        """
        Delete a notification.
        
        Args:
            notification_id: Notification ID
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if notification belongs to user
            notification_response = self.supabase.table("notifications").select("user_id").eq("id", notification_id).execute()
            
            if not notification_response.data:
                logger.error(f"Notification not found: {notification_id}")
                return False
            
            notification_user_id = notification_response.data[0]["user_id"]
            
            if notification_user_id != str(user_id):
                logger.error(f"Notification {notification_id} does not belong to user {user_id}")
                return False
            
            # Delete notification
            self.supabase.table("notifications").delete().eq("id", notification_id).execute()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting notification: {str(e)}")
            return False

# Create notification service instance
notification_service = NotificationService()
