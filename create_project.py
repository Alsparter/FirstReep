#!/usr/bin/env python3
"""
AI Interview System - Project Generator
Creates all project files automatically
"""

import os

def create_file(filename, content):
    """Create a file with the given content"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filename}")

def main():
    print("🤖 Creating AI Interview System Project...")
    print("=" * 50)
    
    # Create requirements.txt
    requirements = """streamlit==1.29.0
transformers==4.36.0
torch==2.1.0
requests==2.31.0
speech_recognition==3.10.0
pyttsx3==2.90
opencv-python==4.8.1.78
Pillow==10.1.0
numpy==1.24.3
pandas==2.1.3
matplotlib==3.7.2
python-dotenv==1.0.0
streamlit-webrtc==0.47.1
av==10.0.0
streamlit-mic-recorder==0.0.4
streamlit-camera-input-live==0.2.0
ollama==0.1.7
sentence-transformers==2.2.2"""
    create_file("requirements.txt", requirements)
    
    # Create .env.example
    env_example = """# FREE AI Configuration - No API Keys Required! 🎉
# Ollama Local AI Server (recommended)
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2

# Hugging Face Model (fallback)
HUGGINGFACE_MODEL=microsoft/DialoGPT-small

# Audio/Video Settings (Optional)
AUDIO_SAMPLE_RATE=16000
VIDEO_WIDTH=640
VIDEO_HEIGHT=480
VIDEO_FPS=30"""
    create_file(".env.example", env_example)
    
    # Create config.py
    config_py = """import os
from typing import Dict, List

# AI Configuration
# Using Free Local AI Models - No API Keys Required!
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama2")  # Free Ollama model
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-large")  # Free HF model

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
}"""
    create_file("config.py", config_py)
    
    print("\n🎉 Project files created successfully!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. (Optional) Set up Ollama: python setup_ollama.py")
    print("3. Run the app: python run_app.py")
    print("\n🆓 Completely FREE - no API keys required!")

if __name__ == "__main__":
    main()