from typing import Dict
from uuid import UUID

from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.services.db import get_supabase_client

def analyze_learning_style(user_id: UUID) -> Dict:
    """
    Analyze a user's learning style based on their activity.
    This uses LangChain to generate a learning style profile.
    """
    supabase = get_supabase_client()
    
    # Get user's quiz submissions
    quiz_submissions = supabase.table("quiz_submissions").select("*").eq("user_id", str(user_id)).execute()
    
    # Get user's progress data
    progress_data = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).execute()
    
    # Get content items that the user has interacted with
    content_ids = [p["content_id"] for p in progress_data.data]
    content_items = []
    for content_id in content_ids:
        content = supabase.table("content_items").select("*").eq("content_id", content_id).execute()
        if content.data:
            content_items.append(content.data[0])
    
    # Use LangChain to analyze learning style
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.7, "max_length": 500}
    )
    
    prompt = PromptTemplate(
        input_variables=["quiz_submissions", "progress_data", "content_items"],
        template="""
        Based on the user's quiz submissions: {quiz_submissions}
        And their progress data: {progress_data}
        And the content they've interacted with: {content_items}
        
        Analyze their learning style and preferences. Consider:
        1. Do they prefer visual, auditory, or reading/writing content?
        2. Do they spend more time on certain types of content?
        3. How do they perform on different types of assessments?
        4. What patterns emerge from their learning behavior?
        
        Provide a detailed learning style profile in JSON format with the following structure:
        {
          "primary_style": "visual|auditory|reading|kinesthetic",
          "secondary_style": "visual|auditory|reading|kinesthetic",
          "pace_preference": "fast|moderate|slow",
          "content_preferences": {
            "videos": 1-10 score,
            "text": 1-10 score,
            "interactive": 1-10 score,
            "quizzes": 1-10 score
          },
          "strengths": ["strength1", "strength2"],
          "areas_for_improvement": ["area1", "area2"],
          "recommended_approaches": ["approach1", "approach2"]
        }
        """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # This is a simplified example - in a real application, you would process the data more thoroughly
    result = chain.run(
        quiz_submissions=quiz_submissions.data[:5] if quiz_submissions.data else [],
        progress_data=progress_data.data[:5] if progress_data.data else [],
        content_items=content_items[:5] if content_items else []
    )
    
    # Parse the result and update the user's learning preferences
    # For simplicity, we'll just return a dummy result
    learning_style = {
        "primary_style": "visual",
        "secondary_style": "reading",
        "pace_preference": "moderate",
        "content_preferences": {
            "videos": 8,
            "text": 7,
            "interactive": 6,
            "quizzes": 5
        },
        "strengths": ["visual pattern recognition", "detail orientation"],
        "areas_for_improvement": ["auditory processing", "group learning"],
        "recommended_approaches": ["use diagrams and charts", "take detailed notes"]
    }
    
    # Update the user's learning preferences in the database
    supabase.table("users").update({"learning_preferences": learning_style}).eq("user_id", str(user_id)).execute()
    
    return learning_style
