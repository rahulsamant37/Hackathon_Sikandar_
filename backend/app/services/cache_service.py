"""
Cache service for the application.
"""

import json
import pickle
from typing import Any, Optional, Union

import redis

from app.core.config import settings
from app.core.logging import logger

class RedisCache:
    """
    Redis cache service.
    """
    
    def __init__(self):
        """
        Initialize the Redis cache service.
        """
        self.redis_url = settings.REDIS_URL
        self.client = None
        
        if self.redis_url:
            try:
                self.client = redis.from_url(self.redis_url)
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Redis cache: {str(e)}")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.client:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                try:
                    # Try to deserialize as JSON
                    return json.loads(value)
                except json.JSONDecodeError:
                    try:
                        # Try to deserialize as pickle
                        return pickle.loads(value)
                    except:
                        # Return as is
                        return value
            return None
        except Exception as e:
            logger.error(f"Error getting value from cache: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600,
        use_pickle: bool = False
    ) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (default: 1 hour)
            use_pickle: Whether to use pickle for serialization
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            if use_pickle:
                serialized = pickle.dumps(value)
            else:
                try:
                    serialized = json.dumps(value)
                except (TypeError, OverflowError):
                    serialized = pickle.dumps(value)
                    use_pickle = True
            
            self.client.set(key, serialized, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Error setting value in cache: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting value from cache: {str(e)}")
            return False
    
    def flush(self) -> bool:
        """
        Flush the entire cache.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if the key exists, False otherwise
        """
        if not self.client:
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking if key exists in cache: {str(e)}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment a value in the cache.
        
        Args:
            key: Cache key
            amount: Amount to increment by
            
        Returns:
            New value or None if failed
        """
        if not self.client:
            return None
        
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing value in cache: {str(e)}")
            return None
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set an expiration time for a key.
        
        Args:
            key: Cache key
            seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            return bool(self.client.expire(key, seconds))
        except Exception as e:
            logger.error(f"Error setting expiration for key in cache: {str(e)}")
            return False

# Create cache service instance
cache = RedisCache()
