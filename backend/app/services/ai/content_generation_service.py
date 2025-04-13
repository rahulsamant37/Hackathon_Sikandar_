"""
Service for generating educational content using AI.
"""

from typing import Dict, List, Optional
import json
from uuid import UUID

from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.core.config import settings
from app.services.db import get_supabase_client

def generate_quiz_questions(topic: str, difficulty: str, num_questions: int = 5) -> List[Dict]:
    """
    Generate quiz questions for a given topic.
    
    Args:
        topic: The topic to generate questions for
        difficulty: The difficulty level (easy, medium, hard)
        num_questions: Number of questions to generate
        
    Returns:
        A list of question objects
    """
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.7, "max_length": 2000}
    )
    
    parser = JsonOutputParser()
    
    prompt = PromptTemplate(
        input_variables=["topic", "difficulty", "num_questions"],
        template="""
        Generate {num_questions} multiple-choice quiz questions about {topic} at a {difficulty} difficulty level.
        
        Return the questions in the following JSON format:
        [
          {{
            "text": "Question text",
            "type": "multiple-choice",
            "options": [
              {{ "id": "a", "text": "Option A" }},
              {{ "id": "b", "text": "Option B" }},
              {{ "id": "c", "text": "Option C" }},
              {{ "id": "d", "text": "Option D" }}
            ],
            "correct_answer": {{ "id": "correct_option_id" }},
            "explanation": "Explanation of the correct answer"
          }}
        ]
        
        Make sure:
        1. Questions are clear and concise
        2. All options are plausible
        3. There is only one correct answer
        4. The difficulty level is appropriate
        5. Questions cover different aspects of the topic
        
        Respond with ONLY the JSON array, no additional text.
        """
    )
    
    try:
        result = llm.invoke(
            prompt.format(
                topic=topic,
                difficulty=difficulty,
                num_questions=num_questions
            )
        )
        
        # Parse the result
        try:
            questions = json.loads(result)
            return questions
        except json.JSONDecodeError:
            # If parsing fails, return a simple question
            return [
                {
                    "text": f"What is {topic}?",
                    "type": "multiple-choice",
                    "options": [
                        {"id": "a", "text": "Option A"},
                        {"id": "b", "text": "Option B"},
                        {"id": "c", "text": "Option C"},
                        {"id": "d", "text": "Option D"}
                    ],
                    "correct_answer": {"id": "a"},
                    "explanation": "This is a fallback question."
                }
            ]
    except Exception as e:
        print(f"Error generating quiz questions: {str(e)}")
        return []

def generate_content_summary(content_text: str, max_length: int = 500) -> str:
    """
    Generate a summary of educational content.
    
    Args:
        content_text: The content to summarize
        max_length: Maximum length of the summary in characters
        
    Returns:
        A summary of the content
    """
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.3, "max_length": max_length}
    )
    
    prompt = PromptTemplate(
        input_variables=["content", "max_length"],
        template="""
        Summarize the following educational content in a clear and concise way.
        Keep the summary under {max_length} characters.
        
        Content:
        {content}
        
        Summary:
        """
    )
    
    try:
        result = llm.invoke(
            prompt.format(
                content=content_text,
                max_length=max_length
            )
        )
        
        return result.strip()
    except Exception as e:
        print(f"Error generating content summary: {str(e)}")
        return "Summary generation failed."

def generate_learning_objectives(topic: str, difficulty: str, num_objectives: int = 5) -> List[str]:
    """
    Generate learning objectives for a given topic.
    
    Args:
        topic: The topic to generate objectives for
        difficulty: The difficulty level (beginner, intermediate, advanced)
        num_objectives: Number of objectives to generate
        
    Returns:
        A list of learning objectives
    """
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.5, "max_length": 1000}
    )
    
    prompt = PromptTemplate(
        input_variables=["topic", "difficulty", "num_objectives"],
        template="""
        Generate {num_objectives} learning objectives for a {difficulty} level course on {topic}.
        
        Each learning objective should:
        1. Start with an action verb (e.g., "Explain", "Analyze", "Create")
        2. Be specific and measurable
        3. Focus on what the learner will be able to do
        4. Be appropriate for the {difficulty} level
        
        Format the response as a JSON array of strings:
        ["Objective 1", "Objective 2", ...]
        
        Respond with ONLY the JSON array, no additional text.
        """
    )
    
    try:
        result = llm.invoke(
            prompt.format(
                topic=topic,
                difficulty=difficulty,
                num_objectives=num_objectives
            )
        )
        
        # Parse the result
        try:
            objectives = json.loads(result)
            return objectives
        except json.JSONDecodeError:
            # If parsing fails, extract objectives line by line
            lines = result.strip().split('\n')
            cleaned_lines = [line.strip().strip('"').strip("'") for line in lines if line.strip()]
            
            # Remove any JSON syntax artifacts
            cleaned_lines = [line.strip('[').strip(']').strip(',').strip('"').strip("'") for line in cleaned_lines]
            
            # Filter out empty lines and non-objective lines
            objectives = [line for line in cleaned_lines if len(line) > 10 and not line.startswith('[') and not line.startswith(']')]
            
            return objectives[:num_objectives]
    except Exception as e:
        print(f"Error generating learning objectives: {str(e)}")
        return [f"Understand the basics of {topic}"]

def generate_content_outline(topic: str, num_sections: int = 5) -> Dict:
    """
    Generate an outline for educational content.
    
    Args:
        topic: The topic to generate an outline for
        num_sections: Number of main sections to include
        
    Returns:
        A content outline with sections and subsections
    """
    llm = HuggingFaceHub(
        repo_id=settings.AI_MODEL_NAME,
        model_kwargs={"temperature": 0.6, "max_length": 2000}
    )
    
    prompt = PromptTemplate(
        input_variables=["topic", "num_sections"],
        template="""
        Create a detailed outline for educational content about {topic} with {num_sections} main sections.
        
        Return the outline in the following JSON format:
        {{
          "title": "Main title for the content",
          "description": "Brief description of the content",
          "sections": [
            {{
              "title": "Section 1 Title",
              "subsections": [
                "Subsection 1.1",
                "Subsection 1.2",
                "Subsection 1.3"
              ]
            }},
            {{
              "title": "Section 2 Title",
              "subsections": [
                "Subsection 2.1",
                "Subsection 2.2"
              ]
            }}
          ]
        }}
        
        Make sure:
        1. The content follows a logical progression
        2. Each section builds on previous sections
        3. The outline covers the topic comprehensively
        4. Subsections provide more detailed breakdown of each section
        
        Respond with ONLY the JSON object, no additional text.
        """
    )
    
    try:
        result = llm.invoke(
            prompt.format(
                topic=topic,
                num_sections=num_sections
            )
        )
        
        # Parse the result
        try:
            outline = json.loads(result)
            return outline
        except json.JSONDecodeError:
            # If parsing fails, return a simple outline
            return {
                "title": f"Introduction to {topic}",
                "description": f"A comprehensive guide to understanding {topic}",
                "sections": [
                    {
                        "title": f"What is {topic}?",
                        "subsections": [
                            "Definition and basic concepts",
                            "Historical context",
                            "Importance and applications"
                        ]
                    },
                    {
                        "title": "Key Principles",
                        "subsections": [
                            "Fundamental principles",
                            "Core components",
                            "Best practices"
                        ]
                    }
                ]
            }
    except Exception as e:
        print(f"Error generating content outline: {str(e)}")
        return {
            "title": f"Introduction to {topic}",
            "description": "Content generation failed",
            "sections": []
        }
