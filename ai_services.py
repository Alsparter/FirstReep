import openai
import json
import speech_recognition as sr
import pyttsx3
import threading
import time
from typing import Dict, List, Optional
from config import OPENAI_API_KEY, AI_PERSONALITIES, SCORING_CRITERIA

class AIInterviewer:
    def __init__(self, personality: str = "Friendly"):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.personality = AI_PERSONALITIES.get(personality, AI_PERSONALITIES["Friendly"])
        self.conversation_history = []
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Try to set a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        self.tts_engine.setProperty('rate', 150)  # Speech rate
        self.tts_engine.setProperty('volume', 0.8)  # Volume level
    
    def generate_response(self, user_input: str, role: str, context: Dict) -> str:
        """Generate AI response based on user input and context"""
        system_prompt = f"""
        {self.personality['prompt']}
        
        You are interviewing a candidate for the position of {role}.
        Keep responses conversational and under 100 words.
        Ask follow-up questions naturally.
        Be encouraging and professional.
        
        Current interview context:
        - Candidate name: {context.get('name', 'Unknown')}
        - Role: {role}
        - Question number: {context.get('current_question', 1)}
        """
        
        messages = [
            {"role": "system", "content": system_prompt}
        ] + self.conversation_history + [
            {"role": "user", "content": user_input}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing that. Could you please repeat your answer?"
    
    def speak_text(self, text: str):
        """Convert text to speech"""
        def speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        # Run TTS in a separate thread to avoid blocking
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
        return thread
    
    def generate_follow_up_question(self, answer: str, role: str, question: str) -> str:
        """Generate a follow-up question based on the candidate's answer"""
        prompt = f"""
        Based on this interview context:
        - Role: {role}
        - Original question: {question}
        - Candidate's answer: {answer}
        
        Generate a brief, natural follow-up question (under 50 words) that:
        1. Builds on their answer
        2. Seeks more specific details
        3. Stays relevant to the role
        
        If the answer was complete, respond with "Thank you for that answer."
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.6
            )
            return response.choices[0].message.content.strip()
        except:
            return "Thank you for that answer."

class SpeechProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen_for_speech(self, timeout: int = 10) -> Optional[str]:
        """Listen for speech and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
                
            print("Processing speech...")
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

class AnswerScorer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def score_answer(self, question: str, answer: str, role: str) -> Dict:
        """Score an answer based on multiple criteria"""
        scoring_prompt = f"""
        Evaluate this interview answer for a {role} position:
        
        Question: {question}
        Answer: {answer}
        
        Rate each criterion from 1-10 and provide brief feedback:
        
        Criteria:
        1. Relevance - How relevant is the answer to the question?
        2. Depth - How detailed and comprehensive is the response?
        3. Communication - How clear and well-structured is the answer?
        4. Experience - How much relevant experience is demonstrated?
        5. Problem-solving - How well does the answer show problem-solving skills?
        
        Return a JSON object with this structure:
        {
            "scores": {
                "relevance": score,
                "depth": score,
                "communication": score,
                "experience": score,
                "problem_solving": score
            },
            "feedback": {
                "relevance": "brief feedback",
                "depth": "brief feedback", 
                "communication": "brief feedback",
                "experience": "brief feedback",
                "problem_solving": "brief feedback"
            },
            "overall_score": average_score,
            "summary": "Overall assessment in 2-3 sentences"
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": scoring_prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            # Fallback scoring if API fails
            return {
                "scores": {criterion: 5 for criterion in SCORING_CRITERIA.keys()},
                "feedback": {criterion: "Unable to evaluate due to technical issues" 
                           for criterion in SCORING_CRITERIA.keys()},
                "overall_score": 5.0,
                "summary": "Technical issues prevented detailed scoring. Please try again."
            }
    
    def generate_final_report(self, all_scores: List[Dict], candidate_name: str, role: str) -> str:
        """Generate a comprehensive final interview report"""
        if not all_scores:
            return "No answers were scored."
        
        # Calculate averages
        criteria = list(all_scores[0]["scores"].keys())
        avg_scores = {}
        for criterion in criteria:
            avg_scores[criterion] = sum(score["scores"][criterion] for score in all_scores) / len(all_scores)
        
        overall_avg = sum(avg_scores.values()) / len(avg_scores)
        
        report_prompt = f"""
        Generate a professional interview report for {candidate_name} applying for {role}:
        
        Average Scores:
        {json.dumps(avg_scores, indent=2)}
        
        Overall Average: {overall_avg:.1f}/10
        
        Individual Answer Summaries:
        {json.dumps([score["summary"] for score in all_scores], indent=2)}
        
        Create a comprehensive report with:
        1. Executive Summary
        2. Strengths
        3. Areas for Improvement  
        4. Recommendation (Hire/Don't Hire/Further Review)
        5. Next Steps
        
        Keep it professional and constructive.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": report_prompt}],
                max_tokens=800,
                temperature=0.4
            )
            return response.choices[0].message.content
        except:
            return f"Interview completed for {candidate_name}. Overall score: {overall_avg:.1f}/10"