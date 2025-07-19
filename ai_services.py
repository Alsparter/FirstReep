import json
import speech_recognition as sr
import pyttsx3
import threading
import time
import requests
from typing import Dict, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, HUGGINGFACE_MODEL, AI_PERSONALITIES, SCORING_CRITERIA

class AIInterviewer:
    def __init__(self, personality: str = "Friendly"):
        self.personality = AI_PERSONALITIES.get(personality, AI_PERSONALITIES["Friendly"])
        self.conversation_history = []
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Initialize free AI models
        self.ollama_available = self._check_ollama_connection()
        self.hf_model = None
        self.hf_tokenizer = None
        
        if not self.ollama_available:
            print("Ollama not available, using Hugging Face model...")
            self._load_huggingface_model()
        
    def _check_ollama_connection(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _load_huggingface_model(self):
        """Load free Hugging Face model as fallback"""
        try:
            print("Loading free AI model from Hugging Face...")
            # Use a smaller, free model for better performance
            model_name = "microsoft/DialoGPT-small"  # Smaller, faster model
            self.hf_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.hf_model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if it doesn't exist
            if self.hf_tokenizer.pad_token is None:
                self.hf_tokenizer.pad_token = self.hf_tokenizer.eos_token
            
            print("✅ Free AI model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Could not load Hugging Face model: {e}")
            self.hf_model = None
            self.hf_tokenizer = None
        
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
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama local model"""
        try:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return "I'm having trouble processing that. Could you please repeat?"
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def _query_huggingface(self, prompt: str) -> str:
        """Query Hugging Face model"""
        if not self.hf_model or not self.hf_tokenizer:
            return "AI model not available. Please check your setup."
        
        try:
            # Encode the prompt
            inputs = self.hf_tokenizer.encode(prompt + self.hf_tokenizer.eos_token, return_tensors='pt')
            
            # Generate response
            with torch.no_grad():
                outputs = self.hf_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 50,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.hf_tokenizer.pad_token_id
                )
            
            # Decode response
            response = self.hf_tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the original prompt from response
            response = response[len(prompt):].strip()
            
            return response if response else "Thank you for your answer. Let's continue."
            
        except Exception as e:
            print(f"Hugging Face error: {e}")
            return "Thank you for sharing that. Let's move forward."
    
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
        
        User said: {user_input}
        
        Respond as an interviewer:
        """
        
        # Try Ollama first, fallback to Hugging Face
        if self.ollama_available:
            ai_response = self._query_ollama(system_prompt)
        else:
            ai_response = self._query_huggingface(system_prompt)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
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
        
        if self.ollama_available:
            return self._query_ollama(prompt)
        else:
            return self._query_huggingface(prompt)

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
            # Convert speech to text using Google's free API
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
        self.ollama_available = self._check_ollama_connection()
        self.scoring_model = None
        
        if not self.ollama_available:
            self._load_scoring_model()
    
    def _check_ollama_connection(self) -> bool:
        """Check if Ollama is available for scoring"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _load_scoring_model(self):
        """Load a free sentiment analysis model for scoring"""
        try:
            print("Loading free scoring model...")
            # Use a free sentiment analysis pipeline
            self.scoring_model = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            print("✅ Free scoring model loaded!")
        except Exception as e:
            print(f"⚠️ Could not load scoring model: {e}")
            self.scoring_model = None
    
    def _generate_fallback_score(self, answer: str) -> Dict:
        """Generate basic scoring when AI models are unavailable"""
        # Simple heuristic scoring
        word_count = len(answer.split())
        
        # Basic scoring based on length and content
        relevance = min(10, max(1, word_count // 5))
        depth = min(10, max(1, word_count // 8))
        communication = min(10, max(1, 8 if word_count > 20 else 5))
        experience = min(10, max(1, 6 if any(word in answer.lower() for word in ['experience', 'worked', 'project', 'team']) else 4))
        problem_solving = min(10, max(1, 7 if any(word in answer.lower() for word in ['problem', 'solution', 'approach', 'method']) else 5))
        
        scores = {
            "relevance": relevance,
            "depth": depth,
            "communication": communication,
            "experience": experience,
            "problem_solving": problem_solving
        }
        
        overall_score = sum(scores.values()) / len(scores)
        
        return {
            "scores": scores,
            "feedback": {
                "relevance": "Answer addresses the question appropriately",
                "depth": "Good level of detail provided",
                "communication": "Clear and well-structured response",
                "experience": "Demonstrates relevant background",
                "problem_solving": "Shows analytical thinking"
            },
            "overall_score": overall_score,
            "summary": f"Solid response with {word_count} words. Shows understanding of the topic and provides relevant details."
        }
    
    def score_answer(self, question: str, answer: str, role: str) -> Dict:
        """Score an answer based on multiple criteria"""
        scoring_prompt = f"""
        Evaluate this interview answer for a {role} position:
        
        Question: {question}
        Answer: {answer}
        
        Rate each criterion from 1-10:
        1. Relevance - How relevant is the answer to the question?
        2. Depth - How detailed and comprehensive is the response?
        3. Communication - How clear and well-structured is the answer?
        4. Experience - How much relevant experience is demonstrated?
        5. Problem-solving - How well does the answer show problem-solving skills?
        
        Provide scores and brief feedback for each criterion.
        Overall assessment should be 2-3 sentences.
        """
        
        try:
            if self.ollama_available:
                # Use Ollama for detailed scoring
                response_text = self._query_ollama_for_scoring(scoring_prompt)
                return self._parse_scoring_response(response_text, answer)
            else:
                # Use fallback scoring method
                return self._generate_fallback_score(answer)
                
        except Exception as e:
            print(f"Scoring error: {e}")
            return self._generate_fallback_score(answer)
    
    def _query_ollama_for_scoring(self, prompt: str) -> str:
        """Query Ollama specifically for scoring"""
        try:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return ""
                
        except Exception as e:
            print(f"Ollama scoring error: {e}")
            return ""
    
    def _parse_scoring_response(self, response_text: str, answer: str) -> Dict:
        """Parse AI response into structured scoring format"""
        try:
            # Try to extract scores from the response
            # This is a simplified parser - in practice you'd want more robust parsing
            scores = {}
            feedback = {}
            
            # Default scores if parsing fails
            default_scores = {
                "relevance": 7,
                "depth": 6,
                "communication": 7,
                "experience": 6,
                "problem_solving": 6
            }
            
            # Simple keyword-based scoring extraction
            for criterion in SCORING_CRITERIA.keys():
                if criterion in response_text.lower():
                    # Try to find a number near the criterion
                    import re
                    pattern = f"{criterion}.*?([1-9]|10)"
                    match = re.search(pattern, response_text.lower())
                    if match:
                        scores[criterion] = int(match.group(1))
                    else:
                        scores[criterion] = default_scores[criterion]
                    
                    feedback[criterion] = f"Good demonstration of {criterion}"
                else:
                    scores[criterion] = default_scores[criterion]
                    feedback[criterion] = f"Shows {criterion} in the response"
            
            overall_score = sum(scores.values()) / len(scores)
            
            return {
                "scores": scores,
                "feedback": feedback,
                "overall_score": overall_score,
                "summary": f"Comprehensive answer that demonstrates good understanding. Total word count: {len(answer.split())} words."
            }
            
        except Exception as e:
            print(f"Parsing error: {e}")
            return self._generate_fallback_score(answer)
    
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
        
        # Generate a comprehensive report
        report = f"""
        # Interview Report for {candidate_name}
        ## Position: {role}
        ## Overall Score: {overall_avg:.1f}/10
        
        ### Performance Summary:
        - **Relevance**: {avg_scores['relevance']:.1f}/10
        - **Depth**: {avg_scores['depth']:.1f}/10  
        - **Communication**: {avg_scores['communication']:.1f}/10
        - **Experience**: {avg_scores['experience']:.1f}/10
        - **Problem-solving**: {avg_scores['problem_solving']:.1f}/10
        
        ### Assessment:
        The candidate demonstrated {'strong' if overall_avg >= 7 else 'good' if overall_avg >= 5 else 'basic'} performance across all evaluation criteria.
        
        ### Recommendation:
        {'Recommended for next round' if overall_avg >= 7 else 'Consider for further evaluation' if overall_avg >= 5 else 'Additional assessment needed'}
        
        ### Next Steps:
        {'Schedule technical interview' if overall_avg >= 7 else 'Review with hiring manager' if overall_avg >= 5 else 'Provide feedback and consider re-interview'}
        """
        
        return report