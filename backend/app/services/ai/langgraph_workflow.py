"""
This module implements a LangGraph workflow for personalized learning recommendations.
"""

from typing import Dict, List, TypedDict, Annotated
import json
from datetime import datetime
from uuid import UUID, uuid4

from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.schema import Document
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from app.core.config import settings
from app.services.db import get_supabase_client

# Define state types
class UserData(TypedDict):
    user_id: str
    learning_preferences: Dict
    completed_content: List[str]
    quiz_results: List[Dict]
    content_interactions: List[Dict]

class ContentData(TypedDict):
    available_content: List[Dict]
    course_structure: Dict

class RecommendationState(TypedDict):
    user_data: UserData
    content_data: ContentData
    analysis: Dict
    recommendations: List[Dict]
    errors: List[str]

# Define the nodes in the graph
def fetch_user_data(state: RecommendationState) -> RecommendationState:
    """
    Fetch user data from the database.
    """
    try:
        user_id = state["user_data"]["user_id"]
        supabase = get_supabase_client()

        # Get user's learning preferences
        user_response = supabase.table("users").select("learning_preferences").eq("user_id", user_id).execute()
        learning_preferences = user_response.data[0]["learning_preferences"] if user_response.data else {}

        # Get user's completed content
        progress_response = supabase.table("user_progress").select("*").eq("user_id", user_id).eq("status", "completed").execute()
        completed_content = [item["content_id"] for item in progress_response.data]

        # Get user's quiz results
        quiz_response = supabase.table("quiz_submissions").select("*").eq("user_id", user_id).execute()
        quiz_results = quiz_response.data

        # Get user's content interactions
        # This could be from a separate table tracking detailed interactions
        content_interactions = []

        # Update state
        state["user_data"].update({
            "learning_preferences": learning_preferences,
            "completed_content": completed_content,
            "quiz_results": quiz_results,
            "content_interactions": content_interactions
        })

        return state
    except Exception as e:
        state["errors"].append(f"Error fetching user data: {str(e)}")
        return state

def fetch_content_data(state: RecommendationState) -> RecommendationState:
    """
    Fetch available content and course structure from the database.
    """
    try:
        supabase = get_supabase_client()

        # Get all content items
        content_response = supabase.table("content_items").select("*").execute()
        available_content = content_response.data

        # Get course structure (courses and their modules)
        courses_response = supabase.table("courses").select("*").execute()
        modules_response = supabase.table("modules").select("*").execute()

        # Build course structure
        course_structure = {}
        for course in courses_response.data:
            course_id = course["course_id"]
            course_structure[course_id] = {
                "title": course["title"],
                "modules": {}
            }

        for module in modules_response.data:
            course_id = module["course_id"]
            module_id = module["module_id"]
            if course_id in course_structure:
                course_structure[course_id]["modules"][module_id] = {
                    "title": module["title"],
                    "sequence_number": module["sequence_number"]
                }

        # Update state
        state["content_data"].update({
            "available_content": available_content,
            "course_structure": course_structure
        })

        return state
    except Exception as e:
        state["errors"].append(f"Error fetching content data: {str(e)}")
        return state

def analyze_learning_patterns(state: RecommendationState) -> RecommendationState:
    """
    Analyze user's learning patterns using LLM.
    """
    try:
        # Skip if there are errors or insufficient data
        if state["errors"] or not state["user_data"]["learning_preferences"]:
            return state

        # Use LLM to analyze learning patterns
        llm = HuggingFaceHub(
            repo_id=settings.AI_MODEL_NAME,
            model_kwargs={"temperature": 0.7, "max_length": 500}
        )

        prompt = PromptTemplate(
            input_variables=["learning_preferences", "quiz_results", "content_interactions"],
            template="""
            Based on the user's learning preferences: {learning_preferences}
            Their quiz results: {quiz_results}
            And their content interactions: {content_interactions}

            Analyze their learning patterns and provide insights in JSON format with the following structure:
            {
              "learning_style_insights": {
                "strengths": ["strength1", "strength2"],
                "challenges": ["challenge1", "challenge2"]
              },
              "content_preferences": {
                "preferred_formats": ["format1", "format2"],
                "engagement_patterns": ["pattern1", "pattern2"]
              },
              "knowledge_gaps": ["gap1", "gap2"],
              "recommended_learning_strategies": ["strategy1", "strategy2"]
            }

            Respond with ONLY the JSON object, no additional text.
            """
        )

        result = llm.invoke(
            prompt.format(
                learning_preferences=json.dumps(state["user_data"]["learning_preferences"]),
                quiz_results=json.dumps(state["user_data"]["quiz_results"][:5] if state["user_data"]["quiz_results"] else []),
                content_interactions=json.dumps(state["user_data"]["content_interactions"][:5] if state["user_data"]["content_interactions"] else [])
            )
        )

        # Parse the result
        try:
            analysis = json.loads(result)
            state["analysis"] = analysis
        except json.JSONDecodeError:
            # Fallback to a simple analysis if JSON parsing fails
            state["analysis"] = {
                "learning_style_insights": {
                    "strengths": ["visual learning"],
                    "challenges": ["time management"]
                },
                "content_preferences": {
                    "preferred_formats": ["video", "interactive"],
                    "engagement_patterns": ["short sessions"]
                },
                "knowledge_gaps": [],
                "recommended_learning_strategies": ["spaced repetition"]
            }

        return state
    except Exception as e:
        state["errors"].append(f"Error analyzing learning patterns: {str(e)}")
        return state

def generate_recommendations(state: RecommendationState) -> RecommendationState:
    """
    Generate personalized content recommendations.
    """
    try:
        # Skip if there are errors
        if state["errors"]:
            return state

        # Get completed content IDs
        completed_content = set(state["user_data"]["completed_content"])

        # Filter available content to exclude completed items
        available_content = [
            item for item in state["content_data"]["available_content"]
            if item["content_id"] not in completed_content
        ]

        if not available_content:
            state["recommendations"] = []
            return state

        # Use LLM to generate recommendations
        llm = HuggingFaceHub(
            repo_id=settings.AI_MODEL_NAME,
            model_kwargs={"temperature": 0.7, "max_length": 1000}
        )

        parser = JsonOutputParser()

        prompt = PromptTemplate(
            input_variables=["analysis", "available_content", "course_structure"],
            template="""
            Based on the user's learning analysis: {analysis}
            And the available content: {available_content}
            Within this course structure: {course_structure}

            Generate 5 personalized content recommendations in JSON format with the following structure:
            [
              {{
                "content_id": "id of the recommended content",
                "title": "title of the content",
                "reasoning": "explanation of why this content is recommended",
                "relevance_score": a number between 0 and 1 indicating relevance
              }}
            ]

            Prioritize content that:
            1. Matches the user's preferred learning formats
            2. Addresses knowledge gaps
            3. Follows a logical progression in the course structure
            4. Aligns with the user's learning style

            Respond with ONLY the JSON array, no additional text.
            """
        )

        result = llm.invoke(
            prompt.format(
                analysis=json.dumps(state["analysis"]),
                available_content=json.dumps(available_content[:10]),  # Limit to 10 items for context length
                course_structure=json.dumps(state["content_data"]["course_structure"])
            )
        )

        # Parse the result
        try:
            recommendations = json.loads(result)
            # Ensure we have the right format
            validated_recommendations = []
            for rec in recommendations[:5]:  # Limit to 5 recommendations
                if isinstance(rec, dict) and "content_id" in rec and "reasoning" in rec:
                    validated_recommendations.append(rec)
            state["recommendations"] = validated_recommendations
        except json.JSONDecodeError:
            # Fallback to simple recommendations if JSON parsing fails
            state["recommendations"] = [
                {
                    "content_id": item["content_id"],
                    "title": item["title"],
                    "reasoning": "This content matches your learning preferences",
                    "relevance_score": 0.8
                }
                for item in available_content[:5]
            ]

        return state
    except Exception as e:
        state["errors"].append(f"Error generating recommendations: {str(e)}")
        return state

def save_recommendations(state: RecommendationState) -> RecommendationState:
    """
    Save the generated recommendations to the database.
    """
    try:
        # Skip if there are errors or no recommendations
        if state["errors"] or not state["recommendations"]:
            return state

        user_id = state["user_data"]["user_id"]
        supabase = get_supabase_client()

        # Delete existing recommendations for this user
        supabase.table("ai_recommendations").delete().eq("user_id", user_id).execute()

        # Insert new recommendations
        now = datetime.utcnow().isoformat()
        for rec in state["recommendations"]:
            recommendation_id = str(uuid4())
            supabase.table("ai_recommendations").insert({
                "recommendation_id": recommendation_id,
                "user_id": user_id,
                "content_id": rec["content_id"],
                "recommendation_type": "personalized",
                "reasoning": rec["reasoning"],
                "created_at": now,
                "status": "active"
            }).execute()

        return state
    except Exception as e:
        state["errors"].append(f"Error saving recommendations: {str(e)}")
        return state

def should_end(state: RecommendationState) -> str:
    """
    Determine if the workflow should end.
    """
    if state["errors"]:
        return "error"
    return "continue"

# Create the graph
def create_recommendation_workflow():
    """
    Create a LangGraph workflow for generating personalized recommendations.
    """
    # Create a new graph
    workflow = StateGraph(RecommendationState)

    # Add nodes
    workflow.add_node("fetch_user_data", fetch_user_data)
    workflow.add_node("fetch_content_data", fetch_content_data)
    workflow.add_node("analyze_learning_patterns", analyze_learning_patterns)
    workflow.add_node("generate_recommendations", generate_recommendations)
    workflow.add_node("save_recommendations", save_recommendations)

    # Add edges
    workflow.add_edge("fetch_user_data", "fetch_content_data")
    workflow.add_edge("fetch_content_data", "analyze_learning_patterns")
    workflow.add_edge("analyze_learning_patterns", "generate_recommendations")
    workflow.add_edge("generate_recommendations", "save_recommendations")
    workflow.add_edge("save_recommendations", END)

    # Add conditional edges
    workflow.add_conditional_edges(
        "fetch_user_data",
        should_end,
        {
            "error": END,
            "continue": "fetch_content_data"
        }
    )

    workflow.add_conditional_edges(
        "fetch_content_data",
        should_end,
        {
            "error": END,
            "continue": "analyze_learning_patterns"
        }
    )

    # Set entry point
    workflow.set_entry_point("fetch_user_data")

    return workflow.compile()

# Function to run the workflow
def run_recommendation_workflow(user_id: str) -> List[Dict]:
    """
    Run the recommendation workflow for a specific user.
    """
    # Initialize state
    initial_state: RecommendationState = {
        "user_data": {"user_id": user_id, "learning_preferences": {}, "completed_content": [], "quiz_results": [], "content_interactions": []},
        "content_data": {"available_content": [], "course_structure": {}},
        "analysis": {},
        "recommendations": [],
        "errors": []
    }

    # Create and run the workflow
    workflow = create_recommendation_workflow()
    final_state = workflow.invoke(initial_state)

    # Return recommendations or empty list if there were errors
    if final_state["errors"]:
        print(f"Errors during recommendation workflow: {final_state['errors']}")
        return []

    return final_state["recommendations"]
