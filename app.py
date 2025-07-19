import streamlit as st
import time
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Import custom modules
from config import INTERVIEW_ROLES, AI_PERSONALITIES
from ai_services import AIInterviewer, SpeechProcessor, AnswerScorer
from video_recorder import VideoRecorder, FaceDetector

# Page configuration
st.set_page_config(
    page_title="AI Interview System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e7d32;
        margin: 1rem 0;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .answer-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin: 1rem 0;
    }
    .score-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #ff9800;
        margin: 1rem 0;
    }
    .camera-frame {
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'page': 'setup',
        'candidate_name': '',
        'selected_role': '',
        'ai_personality': 'Friendly',
        'current_question_index': 0,
        'questions': [],
        'answers': [],
        'scores': [],
        'interview_started': False,
        'video_recorder': None,
        'face_detector': None,
        'ai_interviewer': None,
        'speech_processor': None,
        'answer_scorer': None,
        'current_question_text': '',
        'current_answer': '',
        'interview_complete': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setup_page():
    """Initial setup page for candidate information and role selection"""
    st.markdown("<h1 class='main-header'>🤖 AI Interview System</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<h2 class='section-header'>Welcome to Your AI Interview</h2>", unsafe_allow_html=True)
        st.write("Please provide your information and select the role you're interviewing for.")
        
        # Two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Information")
            candidate_name = st.text_input("Full Name", 
                                         value=st.session_state.candidate_name,
                                         placeholder="Enter your full name")
            
            st.markdown("### Interview Role")
            selected_role = st.selectbox(
                "Select the position you're applying for:",
                options=list(INTERVIEW_ROLES.keys()),
                index=list(INTERVIEW_ROLES.keys()).index(st.session_state.selected_role) 
                      if st.session_state.selected_role else 0
            )
            
            if selected_role:
                st.info(f"**Role Description:** {INTERVIEW_ROLES[selected_role]['description']}")
        
        with col2:
            st.markdown("### AI Interviewer Style")
            ai_personality = st.selectbox(
                "Choose your preferred interviewer style:",
                options=list(AI_PERSONALITIES.keys()),
                index=list(AI_PERSONALITIES.keys()).index(st.session_state.ai_personality)
            )
            
            if ai_personality:
                st.info(f"**Style:** {AI_PERSONALITIES[ai_personality]['style']}")
            
            st.markdown("### Interview Instructions")
            st.write("""
            📌 **How it works:**
            1. The AI will ask you questions through voice
            2. You can respond using voice or text
            3. Your camera will record the session
            4. Each answer will be scored automatically
            5. You'll receive a detailed report at the end
            """)
        
        # Start interview button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Interview", type="primary", use_container_width=True):
                if candidate_name and selected_role:
                    st.session_state.candidate_name = candidate_name
                    st.session_state.selected_role = selected_role
                    st.session_state.ai_personality = ai_personality
                    st.session_state.questions = INTERVIEW_ROLES[selected_role]['questions']
                    st.session_state.page = 'interview'
                    st.rerun()
                else:
                    st.error("Please fill in all required fields before starting the interview.")

def interview_page():
    """Main interview page with video, AI interaction, and questions"""
    if not st.session_state.candidate_name or not st.session_state.selected_role:
        st.session_state.page = 'setup'
        st.rerun()
    
    # Initialize AI services
    if not st.session_state.ai_interviewer:
        st.session_state.ai_interviewer = AIInterviewer(st.session_state.ai_personality)
        st.session_state.speech_processor = SpeechProcessor()
        st.session_state.answer_scorer = AnswerScorer()
        st.session_state.video_recorder = VideoRecorder()
        st.session_state.face_detector = FaceDetector()
    
    # Header
    st.markdown(f"<h1 class='main-header'>Interview: {st.session_state.selected_role}</h1>", unsafe_allow_html=True)
    st.markdown(f"**Candidate:** {st.session_state.candidate_name} | **Question:** {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}")
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h3 class='section-header'>📹 Interview Recording</h3>", unsafe_allow_html=True)
        
        # Video recording section
        video_placeholder = st.empty()
        
        # Camera controls
        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("📷 Start Recording", type="primary"):
                if st.session_state.video_recorder.start_recording():
                    st.session_state.interview_started = True
                    st.success("Recording started!")
                else:
                    st.error("Failed to start recording. Please check your camera.")
        
        with col1b:
            if st.button("⏹️ Stop Recording"):
                if st.session_state.video_recorder:
                    frames_recorded = st.session_state.video_recorder.stop_recording()
                    st.info(f"Recording stopped. {frames_recorded} frames recorded.")
        
        # Live camera feed
        if st.session_state.video_recorder and st.session_state.interview_started:
            frame = st.session_state.video_recorder.get_current_frame()
            if frame is not None:
                # Apply face detection
                if st.session_state.face_detector:
                    frame_with_faces = st.session_state.face_detector.draw_face_rectangles(frame)
                else:
                    frame_with_faces = frame
                
                video_placeholder.image(frame_with_faces, channels="BGR", use_column_width=True)
        
        # AI Voice Interaction
        st.markdown("<h3 class='section-header'>🎤 AI Voice Interaction</h3>", unsafe_allow_html=True)
        
        if st.session_state.current_question_index < len(st.session_state.questions):
            current_question = st.session_state.questions[st.session_state.current_question_index]
            
            # AI speaks the question
            col1c, col1d = st.columns(2)
            with col1c:
                if st.button("🔊 Ask Question (Voice)", type="secondary"):
                    if st.session_state.ai_interviewer:
                        st.session_state.ai_interviewer.speak_text(current_question)
                        st.session_state.current_question_text = current_question
                        st.success("AI is asking the question...")
            
            with col1d:
                if st.button("🎤 Listen for Answer"):
                    if st.session_state.speech_processor:
                        with st.spinner("Listening for your answer..."):
                            speech_text = st.session_state.speech_processor.listen_for_speech(timeout=30)
                            if speech_text:
                                st.session_state.current_answer = speech_text
                                st.success(f"Captured: {speech_text[:100]}...")
                            else:
                                st.warning("No speech detected. Please try again or use text input.")
    
    with col2:
        st.markdown("<h3 class='section-header'>❓ Interview Questions</h3>", unsafe_allow_html=True)
        
        # Current question display
        if st.session_state.current_question_index < len(st.session_state.questions):
            current_question = st.session_state.questions[st.session_state.current_question_index]
            
            st.markdown(f"""
            <div class='question-box'>
                <strong>Question {st.session_state.current_question_index + 1}:</strong><br>
                {current_question}
            </div>
            """, unsafe_allow_html=True)
            
            # Answer input
            st.markdown("### Your Answer:")
            answer_text = st.text_area(
                "Type your answer here or use voice input:",
                value=st.session_state.current_answer,
                height=200,
                key=f"answer_{st.session_state.current_question_index}"
            )
            
            # Update current answer
            if answer_text != st.session_state.current_answer:
                st.session_state.current_answer = answer_text
            
            # Submit answer
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    if st.session_state.current_answer.strip():
                        # Score the answer
                        with st.spinner("AI is evaluating your answer..."):
                            score = st.session_state.answer_scorer.score_answer(
                                current_question, 
                                st.session_state.current_answer,
                                st.session_state.selected_role
                            )
                        
                        # Store answer and score
                        st.session_state.answers.append(st.session_state.current_answer)
                        st.session_state.scores.append(score)
                        
                        # Move to next question
                        st.session_state.current_question_index += 1
                        st.session_state.current_answer = ""
                        
                        # Check if interview is complete
                        if st.session_state.current_question_index >= len(st.session_state.questions):
                            st.session_state.interview_complete = True
                            st.session_state.page = 'results'
                        
                        st.rerun()
                    else:
                        st.error("Please provide an answer before submitting.")
            
            with col2b:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.answers.append("Skipped")
                    st.session_state.scores.append({
                        "scores": {criterion: 0 for criterion in ["relevance", "depth", "communication", "experience", "problem_solving"]},
                        "overall_score": 0,
                        "summary": "Question was skipped"
                    })
                    st.session_state.current_question_index += 1
                    st.session_state.current_answer = ""
                    
                    if st.session_state.current_question_index >= len(st.session_state.questions):
                        st.session_state.interview_complete = True
                        st.session_state.page = 'results'
                    
                    st.rerun()
        
        # Progress tracking
        st.markdown("### Interview Progress")
        progress = st.session_state.current_question_index / len(st.session_state.questions)
        st.progress(progress)
        st.write(f"Completed: {st.session_state.current_question_index}/{len(st.session_state.questions)} questions")
        
        # Previous answers summary
        if st.session_state.answers:
            st.markdown("### Previous Answers")
            for i, (q, a, s) in enumerate(zip(st.session_state.questions[:len(st.session_state.answers)], 
                                            st.session_state.answers, 
                                            st.session_state.scores)):
                with st.expander(f"Question {i+1} (Score: {s['overall_score']:.1f}/10)"):
                    st.write(f"**Q:** {q}")
                    st.write(f"**A:** {a}")

def results_page():
    """Results page showing comprehensive interview analysis and scores"""
    st.markdown("<h1 class='main-header'>📊 Interview Results</h1>", unsafe_allow_html=True)
    
    if not st.session_state.scores:
        st.error("No interview data found. Please complete the interview first.")
        if st.button("Start New Interview"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_session_state()
            st.rerun()
        return
    
    # Generate final report
    if st.session_state.answer_scorer:
        final_report = st.session_state.answer_scorer.generate_final_report(
            st.session_state.scores,
            st.session_state.candidate_name,
            st.session_state.selected_role
        )
    else:
        final_report = "Report generation unavailable."
    
    # Overall statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_score = sum(score['overall_score'] for score in st.session_state.scores) / len(st.session_state.scores)
        st.metric("Overall Score", f"{avg_score:.1f}/10")
    
    with col2:
        questions_answered = len([a for a in st.session_state.answers if a != "Skipped"])
        st.metric("Questions Answered", f"{questions_answered}/{len(st.session_state.questions)}")
    
    with col3:
        interview_duration = "~30 minutes"  # Placeholder
        st.metric("Interview Duration", interview_duration)
    
    # Detailed breakdown
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Detailed Score Breakdown")
        
        # Create score breakdown table
        criteria_scores = {}
        for criterion in ["relevance", "depth", "communication", "experience", "problem_solving"]:
            scores = [score['scores'][criterion] for score in st.session_state.scores]
            criteria_scores[criterion] = {
                'average': sum(scores) / len(scores),
                'scores': scores
            }
        
        # Display as chart
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        
        criteria = list(criteria_scores.keys())
        averages = [criteria_scores[c]['average'] for c in criteria]
        
        bars = ax.bar(criteria, averages, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        ax.set_ylabel('Average Score')
        ax.set_title('Score Breakdown by Criteria')
        ax.set_ylim(0, 10)
        
        # Add value labels on bars
        for bar, avg in zip(bars, averages):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   f'{avg:.1f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Individual question scores
        st.markdown("### 📝 Individual Question Analysis")
        for i, (question, answer, score) in enumerate(zip(st.session_state.questions, 
                                                          st.session_state.answers, 
                                                          st.session_state.scores)):
            with st.expander(f"Question {i+1}: Score {score['overall_score']:.1f}/10"):
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Your Answer:** {answer}")
                st.markdown(f"**Summary:** {score['summary']}")
                
                # Score breakdown for this question
                col1a, col2a = st.columns(2)
                with col1a:
                    for criterion, score_val in score['scores'].items():
                        st.write(f"• {criterion.title()}: {score_val}/10")
                
                with col2a:
                    for criterion, feedback in score.get('feedback', {}).items():
                        st.write(f"• {criterion.title()}: {feedback}")
    
    with col2:
        st.markdown("### 🎯 Final Assessment")
        st.markdown(f"""
        <div class='score-box'>
            <h4>Overall Rating: {avg_score:.1f}/10</h4>
            <p><strong>Candidate:</strong> {st.session_state.candidate_name}</p>
            <p><strong>Role:</strong> {st.session_state.selected_role}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download report
        if st.button("📄 Download Report", type="primary", use_container_width=True):
            # Create downloadable report
            report_data = {
                'candidate_name': st.session_state.candidate_name,
                'role': st.session_state.selected_role,
                'overall_score': avg_score,
                'questions': st.session_state.questions,
                'answers': st.session_state.answers,
                'scores': st.session_state.scores,
                'final_report': final_report,
                'timestamp': datetime.now().isoformat()
            }
            
            st.download_button(
                label="Download JSON Report",
                data=json.dumps(report_data, indent=2),
                file_name=f"interview_report_{st.session_state.candidate_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Start new interview
        if st.button("🔄 New Interview", use_container_width=True):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_session_state()
            st.rerun()
    
    # Final AI report
    st.markdown("### 🤖 AI Assessment Report")
    st.markdown(final_report)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🤖 AI Interview System")
        st.markdown("---")
        
        # Navigation
        pages = {
            'setup': '🏠 Setup',
            'interview': '🎤 Interview', 
            'results': '📊 Results'
        }
        
        for page_key, page_name in pages.items():
            if st.button(page_name, use_container_width=True):
                if page_key == 'interview' and not st.session_state.candidate_name:
                    st.error("Please complete setup first")
                elif page_key == 'results' and not st.session_state.interview_complete:
                    st.error("Please complete the interview first")
                else:
                    st.session_state.page = page_key
                    st.rerun()
        
        st.markdown("---")
        
        # Current session info
        if st.session_state.candidate_name:
            st.markdown("### Current Session")
            st.write(f"**Name:** {st.session_state.candidate_name}")
            st.write(f"**Role:** {st.session_state.selected_role}")
            st.write(f"**Progress:** {st.session_state.current_question_index}/{len(st.session_state.questions)}")
        
        # Environment setup info
        st.markdown("---")
        st.markdown("### 🔧 Setup Requirements")
        st.markdown("""
        **For full functionality:**
        - Camera permissions for video recording
        - Microphone permissions for voice input
        - OpenAI API key in environment variables
        
        **API Key Setup:**
        ```bash
        export OPENAI_API_KEY="your-key-here"
        ```
        """)
    
    # Route to appropriate page
    if st.session_state.page == 'setup':
        setup_page()
    elif st.session_state.page == 'interview':
        interview_page()
    elif st.session_state.page == 'results':
        results_page()

if __name__ == "__main__":
    main()