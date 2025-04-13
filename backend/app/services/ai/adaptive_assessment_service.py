"""
Service for adaptive assessments that adjust difficulty based on user performance.
"""

from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.services.db import get_supabase_client
from app.services.ai.content_generation_service import generate_quiz_questions

class AdaptiveAssessmentEngine:
    """
    Engine for creating and managing adaptive assessments.
    """

    def __init__(self, user_id: UUID, course_id: str):
        """
        Initialize the adaptive assessment engine.

        Args:
            user_id: The ID of the user taking the assessment
            course_id: The ID of the course the assessment is for
        """
        self.user_id = user_id
        self.course_id = course_id
        self.supabase = get_supabase_client()
        self.llm = HuggingFaceHub(
            repo_id=settings.AI_MODEL_NAME,
            model_kwargs={"temperature": 0.5, "max_length": 1000}
        )

    def get_user_knowledge_state(self) -> Dict:
        """
        Get the current knowledge state of the user.

        Returns:
            A dictionary representing the user's knowledge state
        """
        # Get user's quiz submissions for this course
        quiz_submissions = self.supabase.table("quiz_submissions").select("*").eq("user_id", str(self.user_id)).execute()

        # Get content progress for this course
        progress = self.supabase.table("user_progress").select("*").eq("user_id", str(self.user_id)).eq("course_id", self.course_id).execute()

        # Get course modules and content
        modules = self.supabase.table("modules").select("*").eq("course_id", self.course_id).execute()

        # Build knowledge state
        knowledge_state = {
            "topics_mastered": [],
            "topics_in_progress": [],
            "topics_not_started": [],
            "average_quiz_score": 0,
            "strengths": [],
            "weaknesses": []
        }

        # Process quiz submissions to identify strengths and weaknesses
        if quiz_submissions.data:
            scores = [sub["score"] for sub in quiz_submissions.data]
            knowledge_state["average_quiz_score"] = sum(scores) / len(scores)

            # Analyze quiz answers to identify strengths and weaknesses
            for submission in quiz_submissions.data:
                quiz_id = submission["quiz_id"]

                # Get quiz details
                quiz = self.supabase.table("quizzes").select("*").eq("quiz_id", quiz_id).execute()
                if not quiz.data:
                    continue

                content_id = quiz.data[0]["content_id"]

                # Get content details
                content = self.supabase.table("content_items").select("*").eq("content_id", content_id).execute()
                if not content.data:
                    continue

                module_id = content.data[0]["module_id"]

                # Get module details
                module = self.supabase.table("modules").select("*").eq("module_id", module_id).execute()
                if not module.data:
                    continue

                topic = module.data[0]["title"]

                # Analyze answers
                answers = submission["answers"]
                correct_count = sum(1 for answer in answers if answer.get("is_correct", False))
                total_count = len(answers)

                if correct_count / total_count >= 0.8:
                    if topic not in knowledge_state["topics_mastered"]:
                        knowledge_state["topics_mastered"].append(topic)

                    # Add to strengths if not already present
                    if topic not in knowledge_state["strengths"]:
                        knowledge_state["strengths"].append(topic)
                elif correct_count / total_count <= 0.4:
                    # Add to weaknesses if not already present
                    if topic not in knowledge_state["weaknesses"]:
                        knowledge_state["weaknesses"].append(topic)

                    if topic not in knowledge_state["topics_in_progress"]:
                        knowledge_state["topics_in_progress"].append(topic)
                else:
                    if topic not in knowledge_state["topics_in_progress"]:
                        knowledge_state["topics_in_progress"].append(topic)

        # Process module progress
        for module in modules.data:
            topic = module["title"]

            if topic not in knowledge_state["topics_mastered"] and topic not in knowledge_state["topics_in_progress"]:
                knowledge_state["topics_not_started"].append(topic)

        return knowledge_state

    def generate_adaptive_assessment(self, num_questions: int = 10) -> Dict:
        """
        Generate an adaptive assessment based on the user's knowledge state.

        Args:
            num_questions: Number of questions to include in the assessment

        Returns:
            An assessment object with questions
        """
        knowledge_state = self.get_user_knowledge_state()

        # Determine question distribution based on knowledge state
        question_distribution = self._calculate_question_distribution(knowledge_state, num_questions)

        # Generate questions for each topic and difficulty
        questions = []

        for topic, difficulties in question_distribution.items():
            for difficulty, count in difficulties.items():
                if count > 0:
                    topic_questions = generate_quiz_questions(topic, difficulty, count)
                    questions.extend(topic_questions)

        # Create assessment
        assessment_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        assessment = {
            "assessment_id": assessment_id,
            "user_id": str(self.user_id),
            "course_id": self.course_id,
            "questions": questions,
            "created_at": now,
            "expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "status": "active"
        }

        # Save assessment to database
        self.supabase.table("adaptive_assessments").insert(assessment).execute()

        # Return assessment without answers for frontend
        frontend_assessment = {
            "assessment_id": assessment_id,
            "questions": [
                {
                    "question_id": str(uuid4()),  # Generate new IDs for frontend
                    "text": q["text"],
                    "type": q["type"],
                    "options": q["options"]
                }
                for q in questions
            ],
            "expires_at": assessment["expires_at"]
        }

        return frontend_assessment

    def _calculate_question_distribution(self, knowledge_state: Dict, num_questions: int) -> Dict:
        """
        Calculate the distribution of questions across topics and difficulties.

        Args:
            knowledge_state: The user's knowledge state
            num_questions: Total number of questions to generate

        Returns:
            A dictionary mapping topics to difficulties and question counts
        """
        distribution = {}

        # Allocate questions to weaknesses (40%)
        weakness_count = int(num_questions * 0.4)
        weakness_per_topic = max(1, weakness_count // len(knowledge_state["weaknesses"])) if knowledge_state["weaknesses"] else 0

        for topic in knowledge_state["weaknesses"]:
            distribution[topic] = {
                "easy": weakness_per_topic // 2,
                "medium": weakness_per_topic // 2,
                "hard": 0
            }

        # Allocate questions to topics in progress (40%)
        in_progress_count = int(num_questions * 0.4)
        in_progress_per_topic = max(1, in_progress_count // len(knowledge_state["topics_in_progress"])) if knowledge_state["topics_in_progress"] else 0

        for topic in knowledge_state["topics_in_progress"]:
            if topic not in distribution:
                distribution[topic] = {
                    "easy": 0,
                    "medium": in_progress_per_topic // 2,
                    "hard": in_progress_per_topic // 2
                }
            else:
                distribution[topic]["medium"] += in_progress_per_topic // 2
                distribution[topic]["hard"] += in_progress_per_topic // 2

        # Allocate questions to mastered topics (20%)
        mastered_count = int(num_questions * 0.2)
        mastered_per_topic = max(1, mastered_count // len(knowledge_state["topics_mastered"])) if knowledge_state["topics_mastered"] else 0

        for topic in knowledge_state["topics_mastered"]:
            if topic not in distribution:
                distribution[topic] = {
                    "easy": 0,
                    "medium": 0,
                    "hard": mastered_per_topic
                }
            else:
                distribution[topic]["hard"] += mastered_per_topic

        # Fill in any remaining questions with not started topics
        remaining_count = num_questions - sum(sum(difficulties.values()) for difficulties in distribution.values())

        if remaining_count > 0 and knowledge_state["topics_not_started"]:
            not_started_per_topic = max(1, remaining_count // len(knowledge_state["topics_not_started"]))

            for topic in knowledge_state["topics_not_started"]:
                distribution[topic] = {
                    "easy": not_started_per_topic,
                    "medium": 0,
                    "hard": 0
                }

        return distribution

    def evaluate_assessment(self, assessment_id: str, answers: List[Dict]) -> Dict:
        """
        Evaluate an assessment submission.

        Args:
            assessment_id: The ID of the assessment
            answers: The user's answers

        Returns:
            Assessment results
        """
        # Get assessment
        assessment_response = self.supabase.table("adaptive_assessments").select("*").eq("assessment_id", assessment_id).execute()

        if not assessment_response.data:
            return {"error": "Assessment not found"}

        assessment = assessment_response.data[0]

        # Check if assessment is expired
        if datetime.utcnow().isoformat() > assessment["expires_at"]:
            return {"error": "Assessment has expired"}

        # Check if assessment belongs to the user
        if assessment["user_id"] != str(self.user_id):
            return {"error": "Unauthorized"}

        # Evaluate answers
        questions = assessment["questions"]
        correct_count = 0
        question_results = []

        for answer in answers:
            question_id = answer["question_id"]
            answer_data = answer["answer_data"]

            # Find the corresponding question
            question = next((q for q in questions if q.get("question_id") == question_id), None)

            if not question:
                continue

            # Check if answer is correct
            is_correct = answer_data == question["correct_answer"]

            if is_correct:
                correct_count += 1

            question_results.append({
                "question_id": question_id,
                "is_correct": is_correct,
                "correct_answer": question["correct_answer"],
                "explanation": question.get("explanation", "")
            })

        # Calculate score
        score = (correct_count / len(answers)) * 100 if answers else 0

        # Save results
        result_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        result = {
            "result_id": result_id,
            "assessment_id": assessment_id,
            "user_id": str(self.user_id),
            "score": score,
            "question_results": question_results,
            "submitted_at": now
        }

        self.supabase.table("assessment_results").insert(result).execute()

        # Update assessment status
        self.supabase.table("adaptive_assessments").update({"status": "completed"}).eq("assessment_id", assessment_id).execute()

        # Generate feedback
        feedback = self._generate_feedback(score, question_results, questions)

        # Return results
        return {
            "result_id": result_id,
            "score": score,
            "question_results": question_results,
            "feedback": feedback
        }

    def _generate_feedback(self, score: float, question_results: List[Dict], questions: List[Dict]) -> Dict:
        """
        Generate personalized feedback based on assessment results.

        Args:
            score: The overall score
            question_results: Results for each question
            questions: The original questions

        Returns:
            Personalized feedback
        """
        # Group questions by topic
        topic_results = {}

        for result in question_results:
            question_id = result["question_id"]
            question = next((q for q in questions if q.get("question_id") == question_id), None)

            if not question:
                continue

            # Extract topic from question text (simplified approach)
            topic = question.get("topic", "General")

            if topic not in topic_results:
                topic_results[topic] = {
                    "correct": 0,
                    "total": 0
                }

            topic_results[topic]["total"] += 1

            if result["is_correct"]:
                topic_results[topic]["correct"] += 1

        # Calculate topic scores
        for topic, results in topic_results.items():
            results["score"] = (results["correct"] / results["total"]) * 100 if results["total"] > 0 else 0

        # Identify strengths and weaknesses
        strengths = [topic for topic, results in topic_results.items() if results["score"] >= 80]
        weaknesses = [topic for topic, results in topic_results.items() if results["score"] <= 50]

        # Generate feedback using LLM
        prompt = PromptTemplate(
            input_variables=["score", "strengths", "weaknesses"],
            template="""
            Generate personalized feedback for a student who scored {score}% on an assessment.

            Their strengths are in: {strengths}
            Their weaknesses are in: {weaknesses}

            Provide:
            1. An encouraging message based on their performance
            2. Specific recommendations for improving in their weak areas
            3. Suggestions for next steps in their learning journey

            Format the response as a JSON object:
            {{
              "message": "Encouraging message",
              "recommendations": ["Recommendation 1", "Recommendation 2", ...],
              "next_steps": ["Next step 1", "Next step 2", ...]
            }}
            """
        )

        try:
            result = self.llm.invoke(
                prompt.format(
                    score=round(score),
                    strengths=", ".join(strengths) if strengths else "None identified",
                    weaknesses=", ".join(weaknesses) if weaknesses else "None identified"
                )
            )

            # Parse the result
            try:
                feedback = json.loads(result)
                return feedback
            except json.JSONDecodeError:
                # If parsing fails, return a simple feedback
                return {
                    "message": f"You scored {round(score)}% on this assessment.",
                    "recommendations": [f"Focus on improving in {weakness}" for weakness in weaknesses] if weaknesses else ["Continue practicing to maintain your knowledge."],
                    "next_steps": ["Review the material and try again."]
                }
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return {
                "message": f"You scored {round(score)}% on this assessment.",
                "recommendations": ["Review the questions you got wrong."],
                "next_steps": ["Continue to the next section."]
            }

def create_adaptive_assessment(user_id: UUID, course_id: str, num_questions: int = 10) -> Dict:
    """
    Create an adaptive assessment for a user.

    Args:
        user_id: The ID of the user
        course_id: The ID of the course
        num_questions: Number of questions to include

    Returns:
        An assessment object
    """
    engine = AdaptiveAssessmentEngine(user_id, course_id)
    return engine.generate_adaptive_assessment(num_questions)

def evaluate_adaptive_assessment(user_id: UUID, assessment_id: str, answers: List[Dict]) -> Dict:
    """
    Evaluate an adaptive assessment submission.

    Args:
        user_id: The ID of the user
        assessment_id: The ID of the assessment
        answers: The user's answers

    Returns:
        Assessment results
    """
    # Get course ID from assessment
    supabase = get_supabase_client()
    assessment_response = supabase.table("adaptive_assessments").select("course_id").eq("assessment_id", assessment_id).execute()

    if not assessment_response.data:
        return {"error": "Assessment not found"}

    course_id = assessment_response.data[0]["course_id"]

    engine = AdaptiveAssessmentEngine(user_id, course_id)
    return engine.evaluate_assessment(assessment_id, answers)
