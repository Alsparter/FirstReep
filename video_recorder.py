import cv2
import streamlit as st
import numpy as np
import time
import threading
from typing import Optional
import queue
from config import VIDEO_CONFIG

class VideoRecorder:
    def __init__(self):
        self.cap = None
        self.is_recording = False
        self.frames = []
        self.recording_thread = None
        self.frame_queue = queue.Queue(maxsize=10)
        
    def initialize_camera(self) -> bool:
        """Initialize the camera"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_CONFIG["width"])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_CONFIG["height"])
            self.cap.set(cv2.CAP_PROP_FPS, VIDEO_CONFIG["fps"])
            
            return True
        except Exception as e:
            st.error(f"Failed to initialize camera: {e}")
            return False
    
    def start_recording(self):
        """Start recording video"""
        if not self.cap or not self.cap.isOpened():
            if not self.initialize_camera():
                st.error("Cannot start recording: Camera not available")
                return False
        
        self.is_recording = True
        self.frames = []
        
        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record_frames)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        return True
    
    def stop_recording(self):
        """Stop recording video"""
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        return len(self.frames)
    
    def _record_frames(self):
        """Internal method to record frames"""
        while self.is_recording and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Add timestamp to frame
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, timestamp, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                self.frames.append(frame)
                
                # Add frame to queue for live display
                if not self.frame_queue.full():
                    try:
                        self.frame_queue.put_nowait(frame)
                    except queue.Full:
                        pass
            
            time.sleep(1/VIDEO_CONFIG["fps"])
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current frame for live display"""
        if not self.cap or not self.cap.isOpened():
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            return None
        except:
            return None
    
    def get_live_frame(self) -> Optional[np.ndarray]:
        """Get frame from the queue for live display"""
        try:
            if not self.frame_queue.empty():
                return self.frame_queue.get_nowait()
            return None
        except queue.Empty:
            return None
    
    def save_recording(self, filename: str) -> bool:
        """Save recorded frames to video file"""
        if not self.frames:
            return False
        
        try:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, VIDEO_CONFIG["fps"], 
                                (VIDEO_CONFIG["width"], VIDEO_CONFIG["height"]))
            
            for frame in self.frames:
                out.write(frame)
            
            out.release()
            return True
        except Exception as e:
            st.error(f"Failed to save recording: {e}")
            return False
    
    def release_camera(self):
        """Release camera resources"""
        self.is_recording = False
        if self.cap:
            self.cap.release()
            self.cap = None

class FaceDetector:
    def __init__(self):
        # Load the face cascade classifier
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            self.face_cascade = None
    
    def detect_face_presence(self, frame: np.ndarray) -> bool:
        """Detect if a face is present in the frame"""
        if self.face_cascade is None:
            return True  # Assume face is present if detector is not available
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            return len(faces) > 0
        except:
            return True
    
    def get_face_analysis(self, frame: np.ndarray) -> dict:
        """Analyze face in the frame and return basic metrics"""
        if self.face_cascade is None:
            return {"faces_detected": 0, "confidence": 0}
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            analysis = {
                "faces_detected": len(faces),
                "confidence": len(faces) > 0,
                "face_positions": []
            }
            
            for (x, y, w, h) in faces:
                analysis["face_positions"].append({
                    "x": int(x), "y": int(y), "width": int(w), "height": int(h)
                })
            
            return analysis
        except:
            return {"faces_detected": 0, "confidence": 0}
    
    def draw_face_rectangles(self, frame: np.ndarray) -> np.ndarray:
        """Draw rectangles around detected faces"""
        if self.face_cascade is None:
            return frame
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            
            return frame
        except:
            return frame