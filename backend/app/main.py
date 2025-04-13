"""
Main application module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logging import logger
from app.core.middleware import setup_middleware
from app.core.monitoring import setup_monitoring

def create_application() -> FastAPI:
    """
    Create the FastAPI application.

    Returns:
        FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up middleware
    setup_middleware(app)

    # Set up monitoring
    setup_monitoring(app)

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def root():
        """
        Root endpoint.
        """
        return {
            "message": "Welcome to the AI Learning Platform API",
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health")
    def health_check():
        """
        Health check endpoint.
        """
        return {"status": "ok"}

    logger.info("Application startup complete")

    return app

app = create_application()
