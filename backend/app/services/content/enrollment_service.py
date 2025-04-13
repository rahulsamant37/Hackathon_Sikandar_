from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.course import Course
from app.services.content.course_service import get_course
from app.services.db import get_supabase_client

def enroll_user_in_course(user_id: UUID, course_id: str) -> bool:
    """
    Enroll a user in a course.
    Returns True if enrollment was successful, False otherwise.
    """
    supabase = get_supabase_client()
    
    # Check if course exists
    course = get_course(course_id=course_id)
    if not course:
        return False
    
    # Check if user is already enrolled
    response = supabase.table("enrollments").select("*").eq("user_id", str(user_id)).eq("course_id", course_id).execute()
    
    if response.data:
        # User is already enrolled
        return True
    
    # Create new enrollment
    enrollment_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    new_enrollment = {
        "enrollment_id": enrollment_id,
        "user_id": str(user_id),
        "course_id": course_id,
        "enrolled_at": now,
        "status": "active"
    }
    
    supabase.table("enrollments").insert(new_enrollment).execute()
    
    return True

def unenroll_user_from_course(user_id: UUID, course_id: str) -> bool:
    """
    Unenroll a user from a course.
    Returns True if unenrollment was successful, False otherwise.
    """
    supabase = get_supabase_client()
    
    # Check if user is enrolled
    response = supabase.table("enrollments").select("*").eq("user_id", str(user_id)).eq("course_id", course_id).execute()
    
    if not response.data:
        # User is not enrolled
        return False
    
    # Update enrollment status to inactive
    supabase.table("enrollments").update({"status": "inactive"}).eq("user_id", str(user_id)).eq("course_id", course_id).execute()
    
    return True

def get_user_enrollments(user_id: UUID) -> List[str]:
    """
    Get all course IDs that a user is enrolled in.
    """
    supabase = get_supabase_client()
    
    response = supabase.table("enrollments").select("course_id").eq("user_id", str(user_id)).eq("status", "active").execute()
    
    return [enrollment["course_id"] for enrollment in response.data]

def get_enrolled_courses(user_id: UUID) -> List[Course]:
    """
    Get all courses that a user is enrolled in.
    """
    supabase = get_supabase_client()
    
    # Get all active enrollments for the user
    enrollments = supabase.table("enrollments").select("course_id").eq("user_id", str(user_id)).eq("status", "active").execute()
    
    course_ids = [enrollment["course_id"] for enrollment in enrollments.data]
    
    # Get course details for each enrollment
    courses = []
    for course_id in course_ids:
        course = get_course(course_id=course_id)
        if course:
            courses.append(course)
    
    return courses

def get_course_enrollments(course_id: str) -> List[dict]:
    """
    Get all users enrolled in a course.
    """
    supabase = get_supabase_client()
    
    # Get all active enrollments for the course
    enrollments = supabase.table("enrollments").select("*").eq("course_id", course_id).eq("status", "active").execute()
    
    # Get user details for each enrollment
    enrollment_details = []
    for enrollment in enrollments.data:
        user_id = enrollment["user_id"]
        user = supabase.table("users").select("user_id, username, email").eq("user_id", user_id).execute()
        
        if user.data:
            enrollment_details.append({
                "enrollment_id": enrollment["enrollment_id"],
                "user_id": user_id,
                "username": user.data[0]["username"],
                "email": user.data[0]["email"],
                "enrolled_at": enrollment["enrolled_at"]
            })
    
    return enrollment_details

def mark_course_completed(user_id: UUID, course_id: str) -> bool:
    """
    Mark a course as completed for a user.
    Returns True if successful, False otherwise.
    """
    supabase = get_supabase_client()
    
    # Check if user is enrolled
    response = supabase.table("enrollments").select("*").eq("user_id", str(user_id)).eq("course_id", course_id).execute()
    
    if not response.data:
        # User is not enrolled
        return False
    
    # Update enrollment with completion date
    now = datetime.utcnow().isoformat()
    supabase.table("enrollments").update({"completed_at": now}).eq("user_id", str(user_id)).eq("course_id", course_id).execute()
    
    return True
