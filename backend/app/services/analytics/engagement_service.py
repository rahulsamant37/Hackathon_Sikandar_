from datetime import datetime, timedelta
from typing import Dict, List
from uuid import UUID

from app.services.db import get_supabase_client

def get_course_engagement_metrics(course_id: str, days: int = 7) -> Dict:
    """
    Get engagement metrics for a course over the specified number of days.
    """
    supabase = get_supabase_client()
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get all enrollments for the course
    enrollments = supabase.table("enrollments").select("*").eq("course_id", course_id).eq("status", "active").execute()
    total_students = len(enrollments.data)
    
    # Get daily active students
    daily_metrics = []
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        next_date = current_date + timedelta(days=1)
        
        # Get user progress updates for this day
        progress_updates = supabase.table("user_progress").select("user_id").eq("course_id", course_id).gte("last_accessed", current_date.isoformat()).lt("last_accessed", next_date.isoformat()).execute()
        
        # Get content views for this day
        content_views = supabase.table("content_views").select("*").eq("course_id", course_id).gte("viewed_at", current_date.isoformat()).lt("viewed_at", next_date.isoformat()).execute()
        
        # Get quiz submissions for this day
        quiz_submissions = supabase.table("quiz_submissions").select("*").eq("course_id", course_id).gte("submitted_at", current_date.isoformat()).lt("submitted_at", next_date.isoformat()).execute()
        
        # Count unique active students
        active_user_ids = set()
        for progress in progress_updates.data:
            active_user_ids.add(progress["user_id"])
        
        for view in content_views.data:
            active_user_ids.add(view["user_id"])
        
        for submission in quiz_submissions.data:
            active_user_ids.add(submission["user_id"])
        
        daily_metrics.append({
            "date": date_str,
            "active_students": len(active_user_ids),
            "content_views": len(content_views.data),
            "quiz_submissions": len(quiz_submissions.data)
        })
        
        current_date = next_date
    
    # Calculate overall metrics
    total_active_students = len(set().union(*[set(day["active_students"]) for day in daily_metrics])) if daily_metrics else 0
    total_content_views = sum(day["content_views"] for day in daily_metrics)
    total_quiz_submissions = sum(day["quiz_submissions"] for day in daily_metrics)
    
    engagement_rate = (total_active_students / total_students * 100) if total_students > 0 else 0
    
    return {
        "total_students": total_students,
        "total_active_students": total_active_students,
        "engagement_rate": engagement_rate,
        "total_content_views": total_content_views,
        "total_quiz_submissions": total_quiz_submissions,
        "daily_metrics": daily_metrics
    }

def get_student_engagement_metrics(user_id: UUID, days: int = 30) -> Dict:
    """
    Get engagement metrics for a student over the specified number of days.
    """
    supabase = get_supabase_client()
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get all enrollments for the student
    enrollments = supabase.table("enrollments").select("*").eq("user_id", str(user_id)).eq("status", "active").execute()
    enrolled_courses = [enrollment["course_id"] for enrollment in enrollments.data]
    
    # Get progress updates in the date range
    progress_updates = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).gte("last_accessed", start_date.isoformat()).lt("last_accessed", end_date.isoformat()).execute()
    
    # Get content views in the date range
    content_views = supabase.table("content_views").select("*").eq("user_id", str(user_id)).gte("viewed_at", start_date.isoformat()).lt("viewed_at", end_date.isoformat()).execute()
    
    # Get quiz submissions in the date range
    quiz_submissions = supabase.table("quiz_submissions").select("*").eq("user_id", str(user_id)).gte("submitted_at", start_date.isoformat()).lt("submitted_at", end_date.isoformat()).execute()
    
    # Calculate active days
    active_days = set()
    
    for progress in progress_updates.data:
        date = datetime.fromisoformat(progress["last_accessed"]).strftime("%Y-%m-%d")
        active_days.add(date)
    
    for view in content_views.data:
        date = datetime.fromisoformat(view["viewed_at"]).strftime("%Y-%m-%d")
        active_days.add(date)
    
    for submission in quiz_submissions.data:
        date = datetime.fromisoformat(submission["submitted_at"]).strftime("%Y-%m-%d")
        active_days.add(date)
    
    # Calculate metrics by course
    course_metrics = {}
    for course_id in enrolled_courses:
        course_progress = [p for p in progress_updates.data if p["course_id"] == course_id]
        course_views = [v for v in content_views.data if v["course_id"] == course_id]
        course_submissions = [s for s in quiz_submissions.data if s["course_id"] == course_id]
        
        # Get course details
        course = supabase.table("courses").select("title").eq("course_id", course_id).execute()
        course_title = course.data[0]["title"] if course.data else "Unknown Course"
        
        course_metrics[course_id] = {
            "course_id": course_id,
            "title": course_title,
            "progress_updates": len(course_progress),
            "content_views": len(course_views),
            "quiz_submissions": len(course_submissions),
            "last_active": max([p["last_accessed"] for p in course_progress] + [v["viewed_at"] for v in course_views] + [s["submitted_at"] for s in course_submissions], default=None)
        }
    
    return {
        "user_id": str(user_id),
        "enrolled_courses": len(enrolled_courses),
        "active_days": len(active_days),
        "activity_rate": len(active_days) / days * 100,
        "total_progress_updates": len(progress_updates.data),
        "total_content_views": len(content_views.data),
        "total_quiz_submissions": len(quiz_submissions.data),
        "course_metrics": list(course_metrics.values())
    }

def get_content_effectiveness_metrics(content_id: str) -> Dict:
    """
    Get effectiveness metrics for a specific content item.
    """
    supabase = get_supabase_client()
    
    # Get content details
    content = supabase.table("content_items").select("*").eq("content_id", content_id).execute()
    if not content.data:
        return {"error": "Content not found"}
    
    content_data = content.data[0]
    content_type = content_data["type"]
    
    # Get views for this content
    views = supabase.table("content_views").select("*").eq("content_id", content_id).execute()
    total_views = len(views.data)
    
    # Get unique viewers
    unique_viewers = set(view["user_id"] for view in views.data)
    
    # Get progress records for this content
    progress = supabase.table("user_progress").select("*").eq("content_id", content_id).execute()
    
    # Calculate completion rate
    completed = [p for p in progress.data if p["status"] == "completed"]
    completion_rate = len(completed) / len(unique_viewers) * 100 if unique_viewers else 0
    
    # Calculate average time spent
    time_spent = [p["time_spent"] for p in progress.data if p.get("time_spent")]
    avg_time_spent = sum(time_spent) / len(time_spent) if time_spent else 0
    
    # For quiz content, get additional metrics
    quiz_metrics = {}
    if content_type == "quiz":
        # Get quiz details
        quiz = supabase.table("quizzes").select("*").eq("content_id", content_id).execute()
        if quiz.data:
            quiz_id = quiz.data[0]["quiz_id"]
            
            # Get submissions for this quiz
            submissions = supabase.table("quiz_submissions").select("*").eq("quiz_id", quiz_id).execute()
            
            # Calculate average score
            scores = [s["score"] for s in submissions.data]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Calculate pass rate
            passing_score = quiz.data[0]["passing_score"]
            passed = [s for s in submissions.data if s["score"] >= passing_score]
            pass_rate = len(passed) / len(submissions.data) * 100 if submissions.data else 0
            
            quiz_metrics = {
                "total_submissions": len(submissions.data),
                "average_score": avg_score,
                "pass_rate": pass_rate
            }
    
    return {
        "content_id": content_id,
        "title": content_data["title"],
        "type": content_type,
        "total_views": total_views,
        "unique_viewers": len(unique_viewers),
        "completion_rate": completion_rate,
        "average_time_spent": avg_time_spent,
        "quiz_metrics": quiz_metrics if content_type == "quiz" else None
    }
