from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.schemas.quiz import Question, Quiz, QuizCreate, QuizSubmission, QuizSubmissionCreate, QuizUpdate
from app.services.db import get_supabase_client

def get_quiz(quiz_id: str) -> Optional[Quiz]:
    """
    Get a specific quiz by ID.
    """
    supabase = get_supabase_client()
    
    # Get quiz data
    quiz_response = supabase.table("quizzes").select("*").eq("quiz_id", quiz_id).execute()
    
    if not quiz_response.data:
        return None
    
    quiz_data = quiz_response.data[0]
    
    # Get questions for this quiz
    questions_response = supabase.table("questions").select("*").eq("quiz_id", quiz_id).execute()
    
    questions = []
    for question_data in questions_response.data:
        questions.append(
            Question(
                question_id=question_data["question_id"],
                quiz_id=question_data["quiz_id"],
                text=question_data["text"],
                type=question_data["type"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                points=question_data["points"],
                created_at=question_data["created_at"]
            )
        )
    
    return Quiz(
        quiz_id=quiz_data["quiz_id"],
        content_id=quiz_data["content_id"],
        title=quiz_data["title"],
        description=quiz_data.get("description"),
        time_limit=quiz_data.get("time_limit"),
        passing_score=quiz_data["passing_score"],
        created_at=quiz_data["created_at"],
        updated_at=quiz_data.get("updated_at"),
        questions=questions
    )

def create_quiz(quiz_in: QuizCreate) -> Quiz:
    """
    Create a new quiz.
    """
    supabase = get_supabase_client()
    
    quiz_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    # Create quiz
    new_quiz = {
        "quiz_id": quiz_id,
        "content_id": str(quiz_in.content_id),
        "title": quiz_in.title,
        "description": quiz_in.description,
        "time_limit": quiz_in.time_limit,
        "passing_score": quiz_in.passing_score,
        "created_at": now
    }
    
    supabase.table("quizzes").insert(new_quiz).execute()
    
    # Create questions
    questions = []
    for question_data in quiz_in.questions:
        question_id = str(uuid4())
        
        new_question = {
            "question_id": question_id,
            "quiz_id": quiz_id,
            "text": question_data.text,
            "type": question_data.type,
            "options": question_data.options,
            "correct_answer": question_data.correct_answer,
            "points": question_data.points,
            "created_at": now
        }
        
        supabase.table("questions").insert(new_question).execute()
        
        questions.append(
            Question(
                question_id=question_id,
                quiz_id=quiz_id,
                text=question_data.text,
                type=question_data.type,
                options=question_data.options,
                correct_answer=question_data.correct_answer,
                points=question_data.points,
                created_at=now
            )
        )
    
    return Quiz(
        quiz_id=quiz_id,
        content_id=quiz_in.content_id,
        title=quiz_in.title,
        description=quiz_in.description,
        time_limit=quiz_in.time_limit,
        passing_score=quiz_in.passing_score,
        created_at=now,
        questions=questions
    )

def update_quiz(quiz_id: str, quiz_in: QuizUpdate) -> Optional[Quiz]:
    """
    Update a quiz.
    """
    supabase = get_supabase_client()
    
    # Get current quiz data
    current_quiz = get_quiz(quiz_id=quiz_id)
    if not current_quiz:
        return None
    
    # Prepare update data
    update_data = {}
    if quiz_in.title is not None:
        update_data["title"] = quiz_in.title
    if quiz_in.description is not None:
        update_data["description"] = quiz_in.description
    if quiz_in.time_limit is not None:
        update_data["time_limit"] = quiz_in.time_limit
    if quiz_in.passing_score is not None:
        update_data["passing_score"] = quiz_in.passing_score
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Update quiz
    supabase.table("quizzes").update(update_data).eq("quiz_id", quiz_id).execute()
    
    # Get updated quiz
    return get_quiz(quiz_id=quiz_id)

def submit_quiz(user_id: UUID, submission: QuizSubmissionCreate) -> QuizSubmission:
    """
    Submit a quiz and calculate the score.
    """
    supabase = get_supabase_client()
    
    # Get quiz data
    quiz = get_quiz(quiz_id=str(submission.quiz_id))
    if not quiz:
        raise ValueError("Quiz not found")
    
    # Calculate score
    total_points = sum(question.points for question in quiz.questions)
    earned_points = 0
    
    # Create a map of question_id to correct_answer for easier lookup
    correct_answers = {str(question.question_id): question.correct_answer for question in quiz.questions}
    
    # Process each answer
    answers_data = []
    for answer in submission.answers:
        question_id = str(answer.question_id)
        if question_id in correct_answers:
            is_correct = answer.answer_data == correct_answers[question_id]
            
            # Find the question to get its points
            question_points = next((q.points for q in quiz.questions if str(q.question_id) == question_id), 1)
            
            if is_correct:
                earned_points += question_points
            
            answer_data = {
                "question_id": question_id,
                "answer_data": answer.answer_data,
                "is_correct": is_correct
            }
            answers_data.append(answer_data)
    
    # Calculate percentage score
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    
    # Create submission record
    submission_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    submission_data = {
        "submission_id": submission_id,
        "user_id": str(user_id),
        "quiz_id": str(submission.quiz_id),
        "score": score,
        "answers": answers_data,
        "submitted_at": now,
        "time_taken": submission.time_taken
    }
    
    supabase.table("quiz_submissions").insert(submission_data).execute()
    
    # Check if this is a passing score and update user progress if needed
    if score >= quiz.passing_score:
        # Get the content_id for this quiz
        content_id = quiz.content_id
        
        # Check if progress record exists
        progress = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).eq("content_id", str(content_id)).execute()
        
        if progress.data:
            # Update existing progress
            supabase.table("user_progress").update({
                "status": "completed",
                "completion_percentage": 100,
                "last_accessed": now
            }).eq("progress_id", progress.data[0]["progress_id"]).execute()
        else:
            # Create new progress record
            progress_id = str(uuid4())
            supabase.table("user_progress").insert({
                "progress_id": progress_id,
                "user_id": str(user_id),
                "content_id": str(content_id),
                "status": "completed",
                "completion_percentage": 100,
                "last_accessed": now,
                "created_at": now
            }).execute()
    
    return QuizSubmission(
        submission_id=submission_id,
        user_id=user_id,
        quiz_id=submission.quiz_id,
        score=score,
        answers=answers_data,
        submitted_at=now,
        time_taken=submission.time_taken
    )
