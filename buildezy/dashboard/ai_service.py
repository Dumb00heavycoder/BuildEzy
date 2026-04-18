import os
import json
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load .env file (it usually sits in the root of the project)
load_dotenv(find_dotenv())

# The user explicitly said the environment variable is 'Gemini_api_key'
API_KEY = os.getenv("Gemini_api_key")

if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_project_details(project_name, project_description):
    """
    Generates structured AI content for a project using Gemini.
    """
    if not API_KEY:
        print("Warning: Gemini_api_key not found in environment.")
        return {
            "todos": ["Setup project structure", "Integrate AI", "Launch frontend"],
            "progress": "Initialization phase started. Ready for implementation tasks.",
            "stats": [{"name": "Planning", "percentage": 20}, {"name": "Design", "percentage": 5}],
            "vision": "A placeholder vision for an amazing application. Please add Gemini API key."
        }

    # Configuration for text generation
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 1024,
    }

    # Model initialization
    model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

    prompt = f"""
    You are an expert product manager and software architect. A user is starting a new software/tech project.
    Project Name: {project_name}
    Project Description: {project_description}

    Please generate the following details about how they should build and track this project. You must output the response as a raw JSON object (do not wrap it in markdown code blocks).

    Return exactly this JSON structure and nothing else:
    {{
        "todos": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"],
        "progress": "A short, encouraging paragraph summarizing the current starting point and next major milestone.",
        "stats": [
            {{"name": "Frontend Architecture", "percentage": 0}},
            {{"name": "Backend Architecture", "percentage": 0}},
            {{"name": "Product Requirements", "percentage": 40}},
            {{"name": "UI/UX Concept", "percentage": 10}}
        ],
        "vision": "A detailed, inspirational paragraph explaining exactly how the final product could look and function."
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up possible markdown wrappers
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return {
            "todos": ["Define core features", "Setup Git repository", "Review technical stack"],
            "progress": "AI was unable to process the details, but you can still start building manually!",
            "stats": [{"name": "Initial Planning", "percentage": 10}],
            "vision": f"Building {project_name}: {project_description}"
        }
