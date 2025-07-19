#!/usr/bin/env python3
"""
AI Interview System Launcher
Launch script for the voice-to-text AI interviewer application.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_environment():
    """Check if the application environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  No virtual environment detected. It's recommended to use a virtual environment.")
    
    # Check for required files
    required_files = ['app.py', 'config.py', 'ai_services.py', 'video_recorder.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    
    # Check for .env file
    if not Path('.env').exists():
        print("⚠️  No .env file found. You'll need to set your OpenAI API key.")
        if Path('.env.example').exists():
            print("   You can copy .env.example to .env and add your API key.")
    else:
        print("✅ Environment file found")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting AI Interview System...")
    print("📝 The application will open in your default web browser")
    print("🎤 Make sure to grant camera and microphone permissions when prompted")
    print("🔑 Don't forget to set your OpenAI API key in the .env file")
    print("-" * 60)
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return True

def main():
    """Main launcher function"""
    print("🤖 AI Interview System Launcher")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Exiting.")
            sys.exit(1)
    
    # Check other key dependencies
    missing_deps = []
    try:
        import openai
    except ImportError:
        missing_deps.append('openai')
    
    try:
        import cv2
    except ImportError:
        missing_deps.append('opencv-python')
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Exiting.")
            sys.exit(1)
    
    # Run the application
    if not run_streamlit():
        sys.exit(1)

if __name__ == "__main__":
    main()