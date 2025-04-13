"""
Service for tracking and analyzing user behavior.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from app.core.config import settings
from app.core.logging import logger
from app.services.cache_service import cache
from app.services.db import get_supabase_client

class UserAnalyticsService:
    """
    Service for tracking and analyzing user behavior.
    """
    
    def __init__(self):
        """
        Initialize the user analytics service.
        """
        self.supabase = get_supabase_client()
        self.enabled = settings.ANALYTICS_ENABLED
    
    def track_event(
        self,
        user_id: UUID,
        event_type: str,
        event_data: Dict,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Track a user event.
        
        Args:
            user_id: User ID
            event_type: Type of event (e.g., page_view, button_click, etc.)
            event_data: Additional data about the event
            session_id: Session ID (optional)
            
        Returns:
            True if the event was tracked successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            now = datetime.utcnow().isoformat()
            
            event = {
                "user_id": str(user_id),
                "event_type": event_type,
                "event_data": event_data,
                "session_id": session_id,
                "timestamp": now,
                "environment": settings.ENVIRONMENT
            }
            
            self.supabase.table("user_events").insert(event).execute()
            
            # Update cache for real-time analytics
            self._update_event_cache(user_id, event_type, event_data)
            
            return True
        except Exception as e:
            logger.error(f"Error tracking event: {str(e)}")
            return False
    
    def _update_event_cache(self, user_id: UUID, event_type: str, event_data: Dict) -> None:
        """
        Update the event cache for real-time analytics.
        
        Args:
            user_id: User ID
            event_type: Type of event
            event_data: Event data
        """
        try:
            # Update user's recent events
            user_events_key = f"user_events:{user_id}"
            recent_events = cache.get(user_events_key) or []
            
            if isinstance(recent_events, list):
                recent_events.append({
                    "event_type": event_type,
                    "event_data": event_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Keep only the 20 most recent events
                if len(recent_events) > 20:
                    recent_events = recent_events[-20:]
                
                cache.set(user_events_key, recent_events, expire=86400)  # 24 hours
            
            # Update global event counters
            event_counter_key = f"event_counter:{event_type}"
            cache.increment(event_counter_key)
            
            # Set expiration if it's a new key
            if cache.get(event_counter_key) == 1:
                cache.expire(event_counter_key, 86400)  # 24 hours
        except Exception as e:
            logger.error(f"Error updating event cache: {str(e)}")
    
    def get_user_activity(self, user_id: UUID, days: int = 30) -> Dict:
        """
        Get a user's activity over a period of time.
        
        Args:
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            User activity data
        """
        if not self.enabled:
            return {"error": "Analytics is disabled"}
        
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get events from the database
            response = self.supabase.table("user_events").select("*").eq("user_id", str(user_id)).gte("timestamp", start_date.isoformat()).lt("timestamp", end_date.isoformat()).execute()
            
            events = response.data
            
            # Group events by type
            event_types = {}
            for event in events:
                event_type = event["event_type"]
                if event_type not in event_types:
                    event_types[event_type] = 0
                event_types[event_type] += 1
            
            # Group events by day
            daily_activity = {}
            for event in events:
                timestamp = datetime.fromisoformat(event["timestamp"])
                day = timestamp.strftime("%Y-%m-%d")
                
                if day not in daily_activity:
                    daily_activity[day] = 0
                daily_activity[day] += 1
            
            # Fill in missing days
            current_date = start_date
            while current_date <= end_date:
                day = current_date.strftime("%Y-%m-%d")
                if day not in daily_activity:
                    daily_activity[day] = 0
                current_date += timedelta(days=1)
            
            # Sort daily activity by date
            sorted_daily_activity = [
                {"date": day, "count": count}
                for day, count in sorted(daily_activity.items())
            ]
            
            return {
                "total_events": len(events),
                "event_types": event_types,
                "daily_activity": sorted_daily_activity
            }
        except Exception as e:
            logger.error(f"Error getting user activity: {str(e)}")
            return {"error": str(e)}
    
    def get_popular_content(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """
        Get the most popular content based on user activity.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of items to return
            
        Returns:
            List of popular content items
        """
        if not self.enabled:
            return []
        
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get content view events
            response = self.supabase.table("user_events").select("*").eq("event_type", "content_view").gte("timestamp", start_date.isoformat()).lt("timestamp", end_date.isoformat()).execute()
            
            events = response.data
            
            # Count views by content ID
            content_views = {}
            for event in events:
                content_id = event["event_data"].get("content_id")
                if not content_id:
                    continue
                
                if content_id not in content_views:
                    content_views[content_id] = 0
                content_views[content_id] += 1
            
            # Sort content by view count
            sorted_content = sorted(
                content_views.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            # Get content details
            popular_content = []
            for content_id, view_count in sorted_content:
                content_response = self.supabase.table("content_items").select("*").eq("content_id", content_id).execute()
                
                if content_response.data:
                    content_data = content_response.data[0]
                    popular_content.append({
                        "content_id": content_id,
                        "title": content_data["title"],
                        "type": content_data["type"],
                        "view_count": view_count
                    })
            
            return popular_content
        except Exception as e:
            logger.error(f"Error getting popular content: {str(e)}")
            return []
    
    def get_user_retention(self, days: int = 30) -> Dict:
        """
        Calculate user retention over a period of time.
        
        Args:
            days: Number of days to look back
            
        Returns:
            User retention data
        """
        if not self.enabled:
            return {"error": "Analytics is disabled"}
        
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get login events
            response = self.supabase.table("user_events").select("*").eq("event_type", "login").gte("timestamp", start_date.isoformat()).lt("timestamp", end_date.isoformat()).execute()
            
            events = response.data
            
            # Group logins by user and day
            user_logins = {}
            for event in events:
                user_id = event["user_id"]
                timestamp = datetime.fromisoformat(event["timestamp"])
                day = timestamp.strftime("%Y-%m-%d")
                
                if user_id not in user_logins:
                    user_logins[user_id] = set()
                user_logins[user_id].add(day)
            
            # Calculate retention by day
            retention_data = []
            for i in range(days):
                day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                
                # Count users who logged in on this day
                users_on_day = sum(1 for logins in user_logins.values() if day in logins)
                
                # Count users who logged in on this day and also logged in later
                retained_users = 0
                for user_id, logins in user_logins.items():
                    if day in logins:
                        # Check if user logged in on a later day
                        for j in range(i + 1, days):
                            later_day = (start_date + timedelta(days=j)).strftime("%Y-%m-%d")
                            if later_day in logins:
                                retained_users += 1
                                break
                
                retention_rate = (retained_users / users_on_day * 100) if users_on_day > 0 else 0
                
                retention_data.append({
                    "date": day,
                    "users": users_on_day,
                    "retained_users": retained_users,
                    "retention_rate": retention_rate
                })
            
            return {
                "total_users": len(user_logins),
                "retention_data": retention_data
            }
        except Exception as e:
            logger.error(f"Error calculating user retention: {str(e)}")
            return {"error": str(e)}

# Create user analytics service instance
user_analytics = UserAnalyticsService()
