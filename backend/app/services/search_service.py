"""
Service for searching courses and content.
"""

from typing import Dict, List, Optional
from uuid import UUID

from app.core.logging import logger
from app.services.cache_service import cache
from app.services.db import get_supabase_client

class SearchService:
    """
    Service for searching courses and content.
    """
    
    def __init__(self):
        """
        Initialize the search service.
        """
        self.supabase = get_supabase_client()
    
    def search_courses(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for courses.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            offset: Offset for pagination
            filters: Additional filters (optional)
            
        Returns:
            List of matching courses
        """
        try:
            # Check cache first
            cache_key = f"search:courses:{query}:{limit}:{offset}:{filters}"
            cached_results = cache.get(cache_key)
            
            if cached_results:
                return cached_results
            
            # Normalize query
            normalized_query = query.lower().strip()
            
            # Build search query
            search_query = self.supabase.table("courses").select("*")
            
            # Add status filter (only published courses)
            search_query = search_query.eq("status", "published")
            
            # Add additional filters
            if filters:
                if "instructor_id" in filters:
                    search_query = search_query.eq("instructor_id", filters["instructor_id"])
            
            # Execute query
            response = search_query.execute()
            
            # Filter results based on query
            results = []
            for course in response.data:
                title = course.get("title", "").lower()
                description = course.get("description", "").lower()
                
                if normalized_query in title or normalized_query in description:
                    results.append(course)
            
            # Sort results by relevance (title match is more relevant than description match)
            results.sort(
                key=lambda c: (
                    normalized_query in c.get("title", "").lower(),
                    c.get("title", "").lower().find(normalized_query),
                    c.get("description", "").lower().find(normalized_query)
                ),
                reverse=True
            )
            
            # Apply pagination
            paginated_results = results[offset:offset + limit]
            
            # Cache results
            cache.set(cache_key, paginated_results, expire=300)  # 5 minutes
            
            return paginated_results
        except Exception as e:
            logger.error(f"Error searching courses: {str(e)}")
            return []
    
    def search_content(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for content.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            offset: Offset for pagination
            filters: Additional filters (optional)
            
        Returns:
            List of matching content items
        """
        try:
            # Check cache first
            cache_key = f"search:content:{query}:{limit}:{offset}:{filters}"
            cached_results = cache.get(cache_key)
            
            if cached_results:
                return cached_results
            
            # Normalize query
            normalized_query = query.lower().strip()
            
            # Build search query
            search_query = self.supabase.table("content_items").select("*")
            
            # Add additional filters
            if filters:
                if "module_id" in filters:
                    search_query = search_query.eq("module_id", filters["module_id"])
                
                if "type" in filters:
                    search_query = search_query.eq("type", filters["type"])
            
            # Execute query
            response = search_query.execute()
            
            # Filter results based on query
            results = []
            for content in response.data:
                title = content.get("title", "").lower()
                content_data = content.get("content", {})
                
                # Check if content matches query
                if normalized_query in title:
                    results.append(content)
                    continue
                
                # Check content data for matches
                if isinstance(content_data, dict):
                    # For text content, check the text
                    if content.get("type") == "text" and "text" in content_data:
                        if normalized_query in content_data["text"].lower():
                            results.append(content)
                            continue
                    
                    # For video content, check the transcript
                    if content.get("type") == "video" and "transcript" in content_data:
                        if normalized_query in content_data["transcript"].lower():
                            results.append(content)
                            continue
            
            # Sort results by relevance (title match is more relevant than content match)
            results.sort(
                key=lambda c: (
                    normalized_query in c.get("title", "").lower(),
                    c.get("title", "").lower().find(normalized_query)
                ),
                reverse=True
            )
            
            # Apply pagination
            paginated_results = results[offset:offset + limit]
            
            # Cache results
            cache.set(cache_key, paginated_results, expire=300)  # 5 minutes
            
            return paginated_results
        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            return []
    
    def search_all(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict:
        """
        Search for courses and content.
        
        Args:
            query: Search query
            limit: Maximum number of results to return per category
            offset: Offset for pagination
            
        Returns:
            Dictionary with courses and content results
        """
        try:
            # Check cache first
            cache_key = f"search:all:{query}:{limit}:{offset}"
            cached_results = cache.get(cache_key)
            
            if cached_results:
                return cached_results
            
            # Search courses and content
            courses = self.search_courses(query, limit, offset)
            content = self.search_content(query, limit, offset)
            
            # Combine results
            results = {
                "courses": courses,
                "content": content
            }
            
            # Cache results
            cache.set(cache_key, results, expire=300)  # 5 minutes
            
            return results
        except Exception as e:
            logger.error(f"Error searching all: {str(e)}")
            return {"courses": [], "content": []}

# Create search service instance
search_service = SearchService()
