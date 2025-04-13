from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.services.db import get_supabase_client

def get_courses(skip: int = 0, limit: int = 100) -> List[Course]:
    supabase = get_supabase_client()
    response = supabase.table("courses").select("*").range(skip, skip + limit - 1).execute()
    
    courses = []
    for course_data in response.data:
        courses.append(
            Course(
                id=course_data["course_id"],
                title=course_data["title"],
                description=course_data.get("description"),
                status=course_data["status"],
                instructor_id=course_data["instructor_id"],
                created_at=course_data["created_at"],
                updated_at=course_data.get("updated_at")
            )
        )
    
    return courses

def get_course(course_id: str) -> Optional[Course]:
    supabase = get_supabase_client()
    response = supabase.table("courses").select("*").eq("course_id", course_id).execute()
    
    if not response.data:
        return None
    
    course_data = response.data[0]
    return Course(
        id=course_data["course_id"],
        title=course_data["title"],
        description=course_data.get("description"),
        status=course_data["status"],
        instructor_id=course_data["instructor_id"],
        created_at=course_data["created_at"],
        updated_at=course_data.get("updated_at")
    )

def create_course(course_in: CourseCreate, instructor_id: UUID) -> Course:
    supabase = get_supabase_client()
    
    course_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    new_course = {
        "course_id": course_id,
        "title": course_in.title,
        "description": course_in.description,
        "status": course_in.status,
        "instructor_id": str(instructor_id),
        "created_at": now
    }
    
    supabase.table("courses").insert(new_course).execute()
    
    return Course(
        id=course_id,
        title=course_in.title,
        description=course_in.description,
        status=course_in.status,
        instructor_id=instructor_id,
        created_at=now
    )

def update_course(course_id: str, course_in: CourseUpdate) -> Optional[Course]:
    supabase = get_supabase_client()
    
    # Get current course data
    current_course = get_course(course_id)
    if not current_course:
        return None
    
    # Prepare update data
    update_data = {}
    if course_in.title is not None:
        update_data["title"] = course_in.title
    if course_in.description is not None:
        update_data["description"] = course_in.description
    if course_in.status is not None:
        update_data["status"] = course_in.status
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Update course
    supabase.table("courses").update(update_data).eq("course_id", course_id).execute()
    
    # Get updated course
    return get_course(course_id)
