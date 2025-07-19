#!/bin/bash

echo "🤖 AI Interview System Setup"
echo "=============================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "Python version: $python_version"

if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.8+ is required. Please upgrade Python."
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv ai_interview_env
source ai_interview_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️ Please edit .env file and add your OpenAI API key!"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate virtual environment: source ai_interview_env/bin/activate"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "🚀 Ready to start interviewing!"