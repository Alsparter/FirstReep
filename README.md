# 🤖 AI Interview System

A comprehensive voice-to-text AI interviewer application that conducts role-based interviews with real-time voice interaction, video recording, and AI-powered scoring.

## ✨ Features

- **Multi-Role Support**: Pre-configured questions for Software Engineer, Data Scientist, Product Manager, Marketing Manager, and UX Designer roles
- **Voice Interaction**: AI speaks questions and processes voice responses
- **Video Recording**: Real-time camera feed with face detection and recording capabilities
- **AI Scoring**: Automated evaluation of answers across multiple criteria
- **Interactive UI**: Beautiful Streamlit interface with real-time progress tracking
- **Comprehensive Reports**: Detailed analysis with downloadable JSON reports

## 🎯 How It Works

1. **Setup Phase**: Enter your name, select your target role, and choose AI interviewer personality
2. **Interview Phase**: 
   - AI asks questions through voice synthesis
   - Respond using voice input or text
   - Camera records your session with face detection
   - Real-time progress tracking
3. **Results Phase**: 
   - AI scores each answer across 5 criteria
   - Detailed breakdown with visual charts
   - Comprehensive final report with recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Webcam and microphone
- **NO API keys required!** 🎉 (Uses free AI models)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-interview-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up FREE AI (Optional but recommended)**
   ```bash
   python setup_ollama.py
   # This installs Ollama for the best free AI experience
   # If you skip this, the app will use Hugging Face models automatically
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Grant camera and microphone permissions when prompted

## 🔧 Configuration

### AI Configuration

**🎉 NO API KEYS REQUIRED!** The system uses completely free AI models:

1. **Ollama (Recommended)** - Local, private, fast AI models
   - Run `python setup_ollama.py` for automatic setup
   - Models run completely offline after download
   - Best performance and privacy

2. **Hugging Face (Automatic Fallback)** - Free cloud models  
   - No setup required, works immediately
   - Slower but requires zero configuration
   - Automatically used if Ollama isn't available

### Available Roles

The system supports these pre-configured roles:

- **Software Engineer**: Programming, debugging, and technical challenges
- **Data Scientist**: ML algorithms, data analysis, and model validation
- **Product Manager**: Feature prioritization, user research, stakeholder management
- **Marketing Manager**: Campaign strategy, digital marketing, metrics
- **UX Designer**: Design process, user research, prototyping tools

### AI Interviewer Personalities

Choose from different interviewer styles:

- **Professional**: Formal and structured approach
- **Friendly**: Casual and conversational style
- **Technical**: Detail-oriented and analytical focus

## 🎮 Usage Guide

### 1. Setup Phase
- Enter your full name
- Select your target role from the dropdown
- Choose your preferred AI interviewer personality
- Click "Start Interview"

### 2. Interview Phase

**Left Panel - Video & Voice:**
- Click "Start Recording" to begin video capture
- Use "Ask Question (Voice)" for AI to speak the question
- Use "Listen for Answer" to respond via voice

**Right Panel - Questions & Text:**
- View current question in the highlighted box
- Type answers in the text area or use voice input
- Submit answers or skip questions as needed
- Track progress with the progress bar

### 3. Results Phase
- View overall score and detailed breakdown
- Analyze individual question scores
- Read comprehensive AI assessment report
- Download detailed JSON report
- Start a new interview session

## 📊 Scoring System

Each answer is evaluated across 5 criteria:

1. **Relevance** (1-10): How well the answer addresses the question
2. **Depth** (1-10): Level of detail and comprehensiveness
3. **Communication** (1-10): Clarity and structure of response
4. **Experience** (1-10): Demonstration of relevant experience
5. **Problem-solving** (1-10): Evidence of analytical thinking

## 🛠️ Technical Architecture

### Core Components

- **`app.py`**: Main Streamlit application with UI logic
- **`ai_services.py`**: OpenAI integration, speech processing, and scoring
- **`video_recorder.py`**: Camera handling and face detection
- **`config.py`**: Configuration settings and role definitions

### Key Technologies

- **Streamlit**: Web interface and user interaction
- **Ollama + Hugging Face**: FREE AI models (no API costs!)
- **Speech Recognition**: Voice-to-text conversion
- **pyttsx3**: Text-to-speech synthesis
- **OpenCV**: Video recording and face detection
- **Matplotlib**: Score visualization

## 🔒 Privacy & Security

- Video recordings are stored locally during the session
- Audio processing happens in real-time without permanent storage
- Interview data can be downloaded as JSON reports
- OpenAI API calls follow their privacy policies

## 🚨 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure camera permissions are granted
- Check if another application is using the camera
- Try refreshing the browser page

**Microphone not detecting speech:**
- Grant microphone permissions
- Check system audio input settings
- Ensure stable internet connection for Google Speech API

**AI model errors:**
- For Ollama: Ensure service is running (`ollama serve`)
- For Hugging Face: Check internet connectivity
- Try running: `python setup_ollama.py` for better performance

**Installation issues:**
- Use Python 3.8+ (some libraries may not work with older versions)
- Try installing with `pip install --upgrade pip` first
- For OpenCV issues on Linux: `sudo apt-get install python3-opencv`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** for making AI accessible and free for everyone
- **Hugging Face** for the amazing free model ecosystem  
- **Streamlit** for the incredible web framework
- **Open source community** for making this project possible

---

**Built with ❤️ for better interview experiences**

For support or questions, please open an issue on GitHub.