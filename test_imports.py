#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality
"""

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        # Test config
        from config import INTERVIEW_ROLES, AI_PERSONALITIES, SCORING_CRITERIA
        print(f"✅ Config loaded: {len(INTERVIEW_ROLES)} roles, {len(AI_PERSONALITIES)} personalities")
        
        # Test AI services (without actual API calls)
        from ai_services import AIInterviewer, SpeechProcessor, AnswerScorer
        print("✅ AI services imported successfully")
        
        # Test video recorder
        from video_recorder import VideoRecorder, FaceDetector
        print("✅ Video recording components imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_data():
    """Test configuration data structure"""
    print("\n🔧 Testing configuration data...")
    
    from config import INTERVIEW_ROLES, AI_PERSONALITIES
    
    # Test roles
    for role_name, role_data in INTERVIEW_ROLES.items():
        questions = role_data.get('questions', [])
        description = role_data.get('description', '')
        if len(questions) > 0 and description:
            print(f"✅ {role_name}: {len(questions)} questions")
        else:
            print(f"❌ {role_name}: Missing data")
            return False
    
    # Test personalities
    for personality_name, personality_data in AI_PERSONALITIES.items():
        style = personality_data.get('style', '')
        prompt = personality_data.get('prompt', '')
        if style and prompt:
            print(f"✅ {personality_name}: {style}")
        else:
            print(f"❌ {personality_name}: Missing data")
            return False
    
    return True

def test_streamlit_structure():
    """Test if the main app can be loaded (without running)"""
    print("\n🎯 Testing Streamlit app structure...")
    
    try:
        # Check if app.py can be imported
        import app
        print("✅ Main app module loaded successfully")
        
        # Check for main function
        if hasattr(app, 'main'):
            print("✅ Main function found")
        else:
            print("❌ Main function not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error loading app: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 AI Interview System - Component Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test config data
    if not test_config_data():
        all_tests_passed = False
    
    # Test streamlit structure
    if not test_streamlit_structure():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n📝 To start the application:")
        print("1. Set up your OpenAI API key in .env file")
        print("2. Run: python run_app.py")
        print("   or: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)