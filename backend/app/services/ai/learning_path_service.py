from typing import Dict, List
from uuid import UUID

from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

from app.core.config import settings
from app.services.db import get_supabase_client
from app.services.content.course_service import get_course
from app.services.content.module_service import get_modules_by_course

def generate_learning_path(user_id: UUID, course_id: str) -> Dict:
    """
    Generate a personalized learning path for a user in a specific course.
    """
    supabase = get_supabase_client()
    
    # Get user's learning preferences
    user_data = supabase.table("users").select("learning_preferences").eq("user_id", str(user_id)).execute()
    learning_preferences = user_data.data[0]["learning_preferences"] if user_data.data else {}
    
    # Get user's progress in this course
    progress_data = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).execute()
    
    # Get course details
    course = get_course(course_id=course_id)
    if not course:
        return {"error": "Course not found"}
    
    # Get modules for this course
    modules = get_modules_by_course(course_id=course_id)
    
    # Get content items for each module
    module_content = {}
    for module in modules:
        module_id = str(module.module_id)
        content_response = supabase.table("content_items").select("*").eq("module_id", module_id).execute()
        module_content[module_id] = content_response.data
    
    # Get quiz results for this user
    quiz_results = supabase.table("quiz_submissions").select("*").eq("user_id", str(user_id)).execute()
    
    # Use LLM to generate a personalized learning path
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.7, "max_length": 1000}
    )
    
    parser = JsonOutputParser()
    
    prompt = PromptTemplate(
        input_variables=["learning_preferences", "progress_data", "course", "modules", "module_content", "quiz_results"],
        template="""
        Based on the user's learning preferences: {learning_preferences}
        Their progress data: {progress_data}
        The course details: {course}
        The course modules: {modules}
        The content in each module: {module_content}
        And their quiz results: {quiz_results}
        
        Generate a personalized learning path for the user in JSON format with the following structure:
        {{
          "recommended_sequence": [
            {{
              "module_id": "id of the module",
              "title": "title of the module",
              "content_items": [
                {{
                  "content_id": "id of the content item",
                  "title": "title of the content item",
                  "type": "type of content",
                  "priority": "high|medium|low",
                  "reason": "reason for recommendation"
                }}
              ]
            }}
          ],
          "focus_areas": [
            {{
              "topic": "topic name",
              "reason": "reason this is a focus area"
            }}
          ],
          "estimated_completion_time": "estimated time to complete in hours",
          "learning_strategy": "recommended learning strategy based on preferences"
        }}
        
        Consider:
        1. The user's learning style and preferences
        2. Their current progress in the course
        3. Areas where they've struggled (based on quiz results)
        4. A logical sequence through the course modules
        5. Prioritizing content that matches their preferred learning format
        
        Respond with ONLY the JSON object, no additional text.
        """
    )
    
    try:
        result = llm.invoke(
            prompt.format(
                learning_preferences=json.dumps(learning_preferences),
                progress_data=json.dumps(progress_data.data[:10] if progress_data.data else []),
                course=json.dumps(course.dict()),
                modules=json.dumps([m.dict() for m in modules]),
                module_content=json.dumps({k: v[:5] for k, v in module_content.items()}),  # Limit content items for context length
                quiz_results=json.dumps(quiz_results.data[:10] if quiz_results.data else [])
            )
        )
        
        # Parse the result
        try:
            learning_path = json.loads(result)
            return learning_path
        except json.JSONDecodeError:
            # Fallback to a simple learning path if JSON parsing fails
            return generate_fallback_learning_path(course_id, modules, module_content)
    except Exception as e:
        print(f"Error generating learning path: {str(e)}")
        return generate_fallback_learning_path(course_id, modules, module_content)

def generate_fallback_learning_path(course_id: str, modules: List, module_content: Dict) -> Dict:
    """
    Generate a fallback learning path when the AI generation fails.
    """
    recommended_sequence = []
    
    # Sort modules by sequence number
    sorted_modules = sorted(modules, key=lambda m: m.sequence_number)
    
    for module in sorted_modules:
        module_id = str(module.module_id)
        content_items = []
        
        if module_id in module_content:
            for content in module_content[module_id]:
                content_items.append({
                    "content_id": content["content_id"],
                    "title": content["title"],
                    "type": content["type"],
                    "priority": "medium",
                    "reason": "Part of the standard course sequence"
                })
        
        recommended_sequence.append({
            "module_id": module_id,
            "title": module.title,
            "content_items": content_items
        })
    
    return {
        "recommended_sequence": recommended_sequence,
        "focus_areas": [
            {
                "topic": "Course fundamentals",
                "reason": "Building a strong foundation is essential"
            }
        ],
        "estimated_completion_time": f"{len(modules) * 2} hours",
        "learning_strategy": "Follow the course modules in sequence"
    }
