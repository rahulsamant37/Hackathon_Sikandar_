"""
Service for analyzing content performance and engagement.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from app.core.config import settings
from app.core.logging import logger
from app.services.db import get_supabase_client

class ContentAnalyticsService:
    """
    Service for analyzing content performance and engagement.
    """
    
    def __init__(self):
        """
        Initialize the content analytics service.
        """
        self.supabase = get_supabase_client()
        self.enabled = settings.ANALYTICS_ENABLED
    
    def get_content_engagement(self, content_id: str) -> Dict:
        """
        Get engagement metrics for a specific content item.
        
        Args:
            content_id: Content ID
            
        Returns:
            Content engagement metrics
        """
        if not self.enabled:
            return {"error": "Analytics is disabled"}
        
        try:
            # Get content details
            content_response = self.supabase.table("content_items").select("*").eq("content_id", content_id).execute()
            
            if not content_response.data:
                return {"error": "Content not found"}
            
            content = content_response.data[0]
            
            # Get view count
            views_response = self.supabase.table("content_views").select("count").eq("content_id", content_id).execute()
            view_count = len(views_response.data)
            
            # Get unique viewers
            unique_viewers_response = self.supabase.table("content_views").select("user_id").eq("content_id", content_id).execute()
            unique_viewers = len(set(view["user_id"] for view in unique_viewers_response.data))
            
            # Get average time spent
            progress_response = self.supabase.table("user_progress").select("*").eq("content_id", content_id).execute()
            
            total_time_spent = sum(progress["time_spent"] or 0 for progress in progress_response.data)
            avg_time_spent = total_time_spent / len(progress_response.data) if progress_response.data else 0
            
            # Get completion rate
            completed_count = sum(1 for progress in progress_response.data if progress["status"] == "completed")
            completion_rate = (completed_count / len(progress_response.data) * 100) if progress_response.data else 0
            
            # Get quiz performance if content is a quiz
            quiz_performance = None
            if content["type"] == "quiz":
                quiz_response = self.supabase.table("quizzes").select("quiz_id").eq("content_id", content_id).execute()
                
                if quiz_response.data:
                    quiz_id = quiz_response.data[0]["quiz_id"]
                    
                    # Get quiz submissions
                    submissions_response = self.supabase.table("quiz_submissions").select("*").eq("quiz_id", quiz_id).execute()
                    
                    submissions = submissions_response.data
                    
                    if submissions:
                        # Calculate average score
                        avg_score = sum(sub["score"] for sub in submissions) / len(submissions)
                        
                        # Calculate average time taken
                        avg_time_taken = sum(sub["time_taken"] for sub in submissions) / len(submissions)
                        
                        # Calculate pass rate
                        quiz_details_response = self.supabase.table("quizzes").select("passing_score").eq("quiz_id", quiz_id).execute()
                        passing_score = quiz_details_response.data[0]["passing_score"] if quiz_details_response.data else 70
                        
                        passed_count = sum(1 for sub in submissions if sub["score"] >= passing_score)
                        pass_rate = (passed_count / len(submissions) * 100)
                        
                        quiz_performance = {
                            "submissions": len(submissions),
                            "avg_score": avg_score,
                            "avg_time_taken": avg_time_taken,
                            "pass_rate": pass_rate
                        }
            
            return {
                "content_id": content_id,
                "title": content["title"],
                "type": content["type"],
                "view_count": view_count,
                "unique_viewers": unique_viewers,
                "avg_time_spent": avg_time_spent,
                "completion_rate": completion_rate,
                "quiz_performance": quiz_performance
            }
        except Exception as e:
            logger.error(f"Error getting content engagement: {str(e)}")
            return {"error": str(e)}
    
    def get_course_engagement(self, course_id: str) -> Dict:
        """
        Get engagement metrics for a course.
        
        Args:
            course_id: Course ID
            
        Returns:
            Course engagement metrics
        """
        if not self.enabled:
            return {"error": "Analytics is disabled"}
        
        try:
            # Get course details
            course_response = self.supabase.table("courses").select("*").eq("course_id", course_id).execute()
            
            if not course_response.data:
                return {"error": "Course not found"}
            
            course = course_response.data[0]
            
            # Get enrollment count
            enrollments_response = self.supabase.table("enrollments").select("count").eq("course_id", course_id).execute()
            enrollment_count = len(enrollments_response.data)
            
            # Get active enrollments
            active_enrollments_response = self.supabase.table("enrollments").select("count").eq("course_id", course_id).eq("status", "active").execute()
            active_enrollment_count = len(active_enrollments_response.data)
            
            # Get completed enrollments
            completed_enrollments_response = self.supabase.table("enrollments").select("count").eq("course_id", course_id).eq("status", "completed").execute()
            completed_enrollment_count = len(completed_enrollments_response.data)
            
            # Calculate completion rate
            completion_rate = (completed_enrollment_count / enrollment_count * 100) if enrollment_count > 0 else 0
            
            # Get modules
            modules_response = self.supabase.table("modules").select("*").eq("course_id", course_id).order("sequence_number").execute()
            modules = modules_response.data
            
            # Get content for each module
            module_engagement = []
            for module in modules:
                module_id = module["module_id"]
                
                # Get content items
                content_response = self.supabase.table("content_items").select("*").eq("module_id", module_id).execute()
                content_items = content_response.data
                
                # Calculate module completion rate
                module_progress = []
                for content in content_items:
                    content_id = content["content_id"]
                    
                    # Get progress for this content
                    progress_response = self.supabase.table("user_progress").select("*").eq("content_id", content_id).execute()
                    progress_items = progress_response.data
                    
                    completed_count = sum(1 for p in progress_items if p["status"] == "completed")
                    content_completion_rate = (completed_count / len(progress_items) * 100) if progress_items else 0
                    
                    module_progress.append({
                        "content_id": content_id,
                        "title": content["title"],
                        "type": content["type"],
                        "completion_rate": content_completion_rate
                    })
                
                # Calculate average completion rate for the module
                avg_completion_rate = sum(p["completion_rate"] for p in module_progress) / len(module_progress) if module_progress else 0
                
                module_engagement.append({
                    "module_id": module_id,
                    "title": module["title"],
                    "sequence_number": module["sequence_number"],
                    "avg_completion_rate": avg_completion_rate,
                    "content_items": module_progress
                })
            
            # Get dropout points (where users stop progressing)
            dropout_points = []
            for i, module in enumerate(module_engagement):
                if i > 0:
                    prev_completion = module_engagement[i-1]["avg_completion_rate"]
                    curr_completion = module["avg_completion_rate"]
                    
                    if curr_completion < prev_completion * 0.7:  # 30% drop in completion rate
                        dropout_points.append({
                            "module_id": module["module_id"],
                            "title": module["title"],
                            "sequence_number": module["sequence_number"],
                            "completion_drop": prev_completion - curr_completion
                        })
            
            return {
                "course_id": course_id,
                "title": course["title"],
                "enrollment_count": enrollment_count,
                "active_enrollment_count": active_enrollment_count,
                "completed_enrollment_count": completed_enrollment_count,
                "completion_rate": completion_rate,
                "module_engagement": module_engagement,
                "dropout_points": dropout_points
            }
        except Exception as e:
            logger.error(f"Error getting course engagement: {str(e)}")
            return {"error": str(e)}
    
    def get_content_difficulty_analysis(self, content_id: str) -> Dict:
        """
        Analyze the difficulty of a content item based on user performance.
        
        Args:
            content_id: Content ID
            
        Returns:
            Content difficulty analysis
        """
        if not self.enabled:
            return {"error": "Analytics is disabled"}
        
        try:
            # Get content details
            content_response = self.supabase.table("content_items").select("*").eq("content_id", content_id).execute()
            
            if not content_response.data:
                return {"error": "Content not found"}
            
            content = content_response.data[0]
            
            # Only analyze quizzes for difficulty
            if content["type"] != "quiz":
                return {"error": "Difficulty analysis is only available for quizzes"}
            
            # Get quiz details
            quiz_response = self.supabase.table("quizzes").select("quiz_id").eq("content_id", content_id).execute()
            
            if not quiz_response.data:
                return {"error": "Quiz not found"}
            
            quiz_id = quiz_response.data[0]["quiz_id"]
            
            # Get quiz submissions
            submissions_response = self.supabase.table("quiz_submissions").select("*").eq("quiz_id", quiz_id).execute()
            submissions = submissions_response.data
            
            if not submissions:
                return {"error": "No submissions found for this quiz"}
            
            # Get questions
            questions_response = self.supabase.table("questions").select("*").eq("quiz_id", quiz_id).execute()
            questions = questions_response.data
            
            # Analyze difficulty of each question
            question_difficulty = []
            for question in questions:
                question_id = question["question_id"]
                
                # Count correct answers for this question
                correct_count = 0
                total_count = 0
                
                for submission in submissions:
                    answers = submission["answers"]
                    
                    for answer in answers:
                        if answer.get("question_id") == question_id:
                            total_count += 1
                            if answer.get("is_correct", False):
                                correct_count += 1
                
                # Calculate difficulty (percentage of incorrect answers)
                difficulty_score = 100 - (correct_count / total_count * 100) if total_count > 0 else 0
                
                # Classify difficulty
                if difficulty_score < 30:
                    difficulty_level = "easy"
                elif difficulty_score < 70:
                    difficulty_level = "medium"
                else:
                    difficulty_level = "hard"
                
                question_difficulty.append({
                    "question_id": question_id,
                    "text": question["text"],
                    "difficulty_score": difficulty_score,
                    "difficulty_level": difficulty_level,
                    "correct_count": correct_count,
                    "total_count": total_count
                })
            
            # Calculate overall quiz difficulty
            avg_difficulty_score = sum(q["difficulty_score"] for q in question_difficulty) / len(question_difficulty)
            
            if avg_difficulty_score < 30:
                overall_difficulty = "easy"
            elif avg_difficulty_score < 70:
                overall_difficulty = "medium"
            else:
                overall_difficulty = "hard"
            
            return {
                "content_id": content_id,
                "title": content["title"],
                "avg_difficulty_score": avg_difficulty_score,
                "overall_difficulty": overall_difficulty,
                "question_difficulty": question_difficulty
            }
        except Exception as e:
            logger.error(f"Error analyzing content difficulty: {str(e)}")
            return {"error": str(e)}

# Create content analytics service instance
content_analytics = ContentAnalyticsService()
