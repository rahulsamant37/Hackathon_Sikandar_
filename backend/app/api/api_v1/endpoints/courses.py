from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.content.course_service import create_course, get_course, get_courses, update_course

router = APIRouter()

@router.get("/", response_model=List[Course])
def read_courses(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve courses.
    """
    return get_courses(skip=skip, limit=limit)

@router.post("/", response_model=Course)
def create_new_course(
    course_in: CourseCreate, 
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new course.
    """
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return create_course(course_in=course_in, instructor_id=current_user.id)

@router.get("/{course_id}", response_model=Course)
def read_course(
    course_id: str, 
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get course by ID.
    """
    course = get_course(course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.put("/{course_id}", response_model=Course)
def update_course_endpoint(
    course_id: str,
    course_in: CourseUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a course.
    """
    course = get_course(course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    if course.instructor_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return update_course(course_id=course_id, course_in=course_in)
