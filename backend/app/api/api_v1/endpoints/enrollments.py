from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.course import Course
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.content.enrollment_service import (
    enroll_user_in_course,
    get_course_enrollments,
    get_enrolled_courses,
    mark_course_completed,
    unenroll_user_from_course
)

router = APIRouter()

@router.post("/{course_id}/enroll")
def enroll_in_course(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enroll the current user in a course.
    """
    result = enroll_user_in_course(user_id=current_user.id, course_id=course_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return {"status": "success", "message": "Successfully enrolled in course"}

@router.post("/{course_id}/unenroll")
def unenroll_from_course(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Unenroll the current user from a course.
    """
    result = unenroll_user_from_course(user_id=current_user.id, course_id=course_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    return {"status": "success", "message": "Successfully unenrolled from course"}

@router.get("/my-courses", response_model=List[Course])
def get_my_courses(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get all courses that the current user is enrolled in.
    """
    return get_enrolled_courses(user_id=current_user.id)

@router.get("/{course_id}/students")
def get_enrolled_students(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get all students enrolled in a course.
    Only available to instructors of the course or admins.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return get_course_enrollments(course_id=course_id)

@router.post("/{course_id}/complete")
def complete_course(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Mark a course as completed for the current user.
    """
    result = mark_course_completed(user_id=current_user.id, course_id=course_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    return {"status": "success", "message": "Course marked as completed"}
