from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth, courses, ai, analytics, modules, content, quiz,
    enrollments, learning_paths, content_generation, adaptive_assessment,
    preferences, notifications, search
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(modules.router, prefix="/modules", tags=["modules"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(quiz.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning-paths"])
api_router.include_router(content_generation.router, prefix="/content-generation", tags=["content-generation"])
api_router.include_router(adaptive_assessment.router, prefix="/adaptive-assessment", tags=["adaptive-assessment"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
