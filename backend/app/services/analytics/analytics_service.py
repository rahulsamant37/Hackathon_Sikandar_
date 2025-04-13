from typing import Dict, List
from uuid import UUID

from app.services.db import get_supabase_client

def get_user_progress(user_id: UUID) -> Dict:
    """
    Get a user's progress across all courses.
    """
    supabase = get_supabase_client()
    
    # Get user's enrollments
    enrollments = supabase.table("enrollments").select("*").eq("user_id", str(user_id)).execute()
    
    # Get user's progress for each course
    progress_data = {}
    for enrollment in enrollments.data:
        course_id = enrollment["course_id"]
        
        # Get course details
        course = supabase.table("courses").select("*").eq("course_id", course_id).execute()
        if not course.data:
            continue
        
        # Get modules for the course
        modules = supabase.table("modules").select("*").eq("course_id", course_id).execute()
        
        # Get user's progress for each module
        module_progress = {}
        for module in modules.data:
            module_id = module["module_id"]
            
            # Get content items for the module
            content_items = supabase.table("content_items").select("*").eq("module_id", module_id).execute()
            
            # Get user's progress for each content item
            content_progress = {}
            for content in content_items.data:
                content_id = content["content_id"]
                
                # Get user's progress for this content item
                user_progress = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).eq("content_id", content_id).execute()
                
                if user_progress.data:
                    content_progress[content_id] = {
                        "status": user_progress.data[0]["status"],
                        "completion_percentage": user_progress.data[0]["completion_percentage"],
                        "last_accessed": user_progress.data[0]["last_accessed"]
                    }
                else:
                    content_progress[content_id] = {
                        "status": "not_started",
                        "completion_percentage": 0,
                        "last_accessed": None
                    }
            
            # Calculate module completion percentage
            completed_items = sum(1 for p in content_progress.values() if p["status"] == "completed")
            total_items = len(content_progress)
            module_completion = (completed_items / total_items * 100) if total_items > 0 else 0
            
            module_progress[module_id] = {
                "title": module["title"],
                "completion_percentage": module_completion,
                "content_progress": content_progress
            }
        
        # Calculate course completion percentage
        module_completion_values = [m["completion_percentage"] for m in module_progress.values()]
        course_completion = sum(module_completion_values) / len(module_completion_values) if module_completion_values else 0
        
        progress_data[course_id] = {
            "title": course.data[0]["title"],
            "completion_percentage": course_completion,
            "module_progress": module_progress
        }
    
    return {
        "user_id": str(user_id),
        "overall_progress": progress_data
    }

def get_course_analytics(course_id: str) -> Dict:
    """
    Get analytics for a specific course.
    """
    supabase = get_supabase_client()
    
    # Get course details
    course = supabase.table("courses").select("*").eq("course_id", course_id).execute()
    if not course.data:
        return {"error": "Course not found"}
    
    # Get all enrollments for the course
    enrollments = supabase.table("enrollments").select("*").eq("course_id", course_id).execute()
    
    # Get all modules for the course
    modules = supabase.table("modules").select("*").eq("course_id", course_id).execute()
    
    # Collect analytics data
    total_students = len(enrollments.data)
    
    # Calculate completion rates
    completion_data = {}
    for module in modules.data:
        module_id = module["module_id"]
        
        # Get content items for the module
        content_items = supabase.table("content_items").select("*").eq("module_id", module_id).execute()
        
        content_completion = {}
        for content in content_items.data:
            content_id = content["content_id"]
            
            # Get all progress records for this content item
            progress_records = supabase.table("user_progress").select("*").eq("content_id", content_id).execute()
            
            completed_count = sum(1 for p in progress_records.data if p["status"] == "completed")
            completion_rate = (completed_count / total_students * 100) if total_students > 0 else 0
            
            content_completion[content_id] = {
                "title": content["title"],
                "type": content["type"],
                "completion_rate": completion_rate,
                "completed_count": completed_count,
                "total_students": total_students
            }
        
        completion_data[module_id] = {
            "title": module["title"],
            "content_completion": content_completion
        }
    
    # Identify struggling students
    struggling_students = []
    for enrollment in enrollments.data:
        user_id = enrollment["user_id"]
        
        # Get user's progress for this course
        user_progress = get_user_progress(user_id)
        
        # If overall completion is less than 30%, consider the student struggling
        if user_id in user_progress and course_id in user_progress[user_id]["overall_progress"]:
            course_progress = user_progress[user_id]["overall_progress"][course_id]
            if course_progress["completion_percentage"] < 30:
                # Get user details
                user = supabase.table("users").select("username, email").eq("user_id", user_id).execute()
                if user.data:
                    struggling_students.append({
                        "user_id": user_id,
                        "username": user.data[0]["username"],
                        "email": user.data[0]["email"],
                        "completion_percentage": course_progress["completion_percentage"]
                    })
    
    return {
        "course_id": course_id,
        "title": course.data[0]["title"],
        "total_students": total_students,
        "module_completion": completion_data,
        "struggling_students": struggling_students
    }
