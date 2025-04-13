from typing import List, Dict
from uuid import UUID

from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.schemas.recommendation import Recommendation
from app.services.db import get_supabase_client
from app.services.ai.langgraph_workflow import run_recommendation_workflow

def get_recommendations_for_user(user_id: UUID) -> List[Recommendation]:
    """
    Get personalized content recommendations for a user.
    This uses LangChain and LangGraph to generate recommendations based on user's learning history.
    """
    supabase = get_supabase_client()

    # First, check if we have cached recommendations
    response = supabase.table("ai_recommendations").select("*").eq("user_id", str(user_id)).execute()

    recommendations = []
    for rec_data in response.data:
        recommendations.append(
            Recommendation(
                id=rec_data["recommendation_id"],
                user_id=rec_data["user_id"],
                content_id=rec_data["content_id"],
                recommendation_type=rec_data["recommendation_type"],
                reasoning=rec_data["reasoning"],
                created_at=rec_data["created_at"],
                status=rec_data["status"]
            )
        )

    # If we have recommendations, return them
    if recommendations:
        return recommendations

    # Otherwise, we need to generate new recommendations using LangGraph workflow
    try:
        # Run the LangGraph recommendation workflow
        workflow_results = run_recommendation_workflow(str(user_id))

        # If we have results from the workflow, they've already been saved to the database
        # So we can just fetch them again
        if workflow_results:
            response = supabase.table("ai_recommendations").select("*").eq("user_id", str(user_id)).execute()

            recommendations = []
            for rec_data in response.data:
                recommendations.append(
                    Recommendation(
                        id=rec_data["recommendation_id"],
                        user_id=rec_data["user_id"],
                        content_id=rec_data["content_id"],
                        recommendation_type=rec_data["recommendation_type"],
                        reasoning=rec_data["reasoning"],
                        created_at=rec_data["created_at"],
                        status=rec_data["status"]
                    )
                )

            return recommendations
    except Exception as e:
        print(f"Error running recommendation workflow: {str(e)}")
        # Fall back to simple recommendations if the workflow fails

    # Fallback approach using simple LangChain if LangGraph workflow fails
    # Get user's learning history
    user_progress = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).execute()

    # Get user's learning preferences
    user_data = supabase.table("users").select("learning_preferences").eq("user_id", str(user_id)).execute()
    learning_preferences = user_data.data[0]["learning_preferences"] if user_data.data else {}

    # Get available content
    content = supabase.table("content_items").select("*").execute()

    # Use LangChain to generate recommendations
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.7, "max_length": 100}
    )

    prompt = PromptTemplate(
        input_variables=["user_progress", "learning_preferences", "available_content"],
        template="""
        Based on the user's learning history: {user_progress}
        And their learning preferences: {learning_preferences}
        Recommend content from the available options: {available_content}

        Provide recommendations in the format:
        Content ID: [ID]
        Reason: [Reason for recommendation]
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    # This is a placeholder - in a real application, you would parse the output and store recommendations
    return []
