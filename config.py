import os
from typing import Dict, List

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Available Roles for Interview
INTERVIEW_ROLES = {
    "Software Engineer": {
        "description": "Full-stack software development position",
        "questions": [
            "Tell me about your experience with programming languages?",
            "How do you approach debugging complex issues?", 
            "Describe a challenging project you've worked on.",
            "What's your experience with version control systems?",
            "How do you ensure code quality in your projects?"
        ]
    },
    "Data Scientist": {
        "description": "Data analysis and machine learning role",
        "questions": [
            "What's your experience with machine learning algorithms?",
            "How do you handle missing data in datasets?",
            "Describe a data science project you're proud of.",
            "What tools do you use for data visualization?",
            "How do you validate your machine learning models?"
        ]
    },
    "Product Manager": {
        "description": "Product strategy and management position",
        "questions": [
            "How do you prioritize product features?",
            "Describe your experience with user research.",
            "How do you handle conflicting stakeholder requirements?",
            "What metrics do you use to measure product success?",
            "Tell me about a product launch you managed."
        ]
    },
    "Marketing Manager": {
        "description": "Digital marketing and brand management role",
        "questions": [
            "How do you develop marketing strategies?",
            "What's your experience with digital marketing channels?",
            "How do you measure marketing campaign effectiveness?",
            "Describe a successful campaign you've managed.",
            "How do you stay updated with marketing trends?"
        ]
    },
    "UX Designer": {
        "description": "User experience and interface design position",
        "questions": [
            "What's your design process for new products?",
            "How do you conduct user research?",
            "Describe a challenging design problem you solved.",
            "What tools do you use for prototyping?",
            "How do you handle design feedback and iterations?"
        ]
    }
}

# AI Personalities for different interview styles
AI_PERSONALITIES = {
    "Professional": {
        "style": "formal and structured",
        "prompt": "You are a professional interviewer conducting a formal job interview. Be courteous, direct, and focus on evaluating the candidate's qualifications."
    },
    "Friendly": {
        "style": "casual and conversational", 
        "prompt": "You are a friendly interviewer who creates a comfortable atmosphere. Be warm, encouraging, and engage in natural conversation while still evaluating the candidate."
    },
    "Technical": {
        "style": "detail-oriented and analytical",
        "prompt": "You are a technical interviewer focusing on deep technical knowledge. Ask follow-up questions and probe for detailed explanations."
    }
}

# Scoring Criteria
SCORING_CRITERIA = {
    "relevance": "How relevant is the answer to the question asked?",
    "depth": "How detailed and comprehensive is the response?", 
    "communication": "How clear and well-structured is the communication?",
    "experience": "How much relevant experience is demonstrated?",
    "problem_solving": "How well does the candidate demonstrate problem-solving skills?"
}

# Audio Settings
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_size": 1024
}

# Video Settings  
VIDEO_CONFIG = {
    "width": 640,
    "height": 480,
    "fps": 30
}