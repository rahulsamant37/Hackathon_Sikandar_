"""
Middleware for the application.
"""

import time
from typing import Callable, Dict

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import logger

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting requests.
    """
    
    def __init__(
        self,
        app: FastAPI,
        rate_limit_per_minute: int = 60,
        exclude_paths: list = None
    ):
        """
        Initialize the rate limit middleware.
        
        Args:
            app: FastAPI application
            rate_limit_per_minute: Maximum number of requests per minute
            exclude_paths: List of paths to exclude from rate limiting
        """
        super().__init__(app)
        self.rate_limit_per_minute = rate_limit_per_minute
        self.exclude_paths = exclude_paths or []
        self.requests: Dict[str, Dict[str, float]] = {}
        self.window_size = 60  # 1 minute in seconds
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and apply rate limiting.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response
        """
        # Skip rate limiting for excluded paths
        for path in self.exclude_paths:
            if request.url.path.startswith(path):
                return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check if client has exceeded rate limit
        current_time = time.time()
        
        if client_ip in self.requests:
            # Clean up old requests
            self.requests[client_ip] = {
                timestamp: count
                for timestamp, count in self.requests[client_ip].items()
                if current_time - float(timestamp) < self.window_size
            }
            
            # Count requests in the current window
            request_count = sum(self.requests[client_ip].values())
            
            if request_count >= self.rate_limit_per_minute:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return Response(
                    content="Rate limit exceeded. Please try again later.",
                    status_code=429,
                    media_type="text/plain"
                )
        else:
            self.requests[client_ip] = {}
        
        # Update request count
        timestamp = str(current_time)
        self.requests[client_ip][timestamp] = self.requests[client_ip].get(timestamp, 0) + 1
        
        # Process the request
        return await call_next(request)

def setup_middleware(app: FastAPI) -> None:
    """
    Set up middleware for the application.
    
    Args:
        app: FastAPI application
    """
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add rate limiting middleware
    app.add_middleware(
        RateLimitMiddleware,
        rate_limit_per_minute=100,
        exclude_paths=["/docs", "/redoc", "/openapi.json"]
    )
    
    logger.info("Middleware setup complete")
