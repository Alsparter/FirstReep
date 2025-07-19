#!/usr/bin/env python3
"""
Ollama Setup Script for AI Interview System
Helps users install and configure Ollama for the best free AI experience.
"""

import subprocess
import sys
import platform
import requests
import time
import os

def check_ollama_installation():
    """Check if Ollama is already installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is already installed!")
            print(f"Version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama not found. Let's install it!")
    return False

def install_ollama():
    """Install Ollama based on the operating system"""
    system = platform.system().lower()
    
    print(f"🔍 Detected OS: {platform.system()}")
    
    if system == "linux":
        print("📥 Installing Ollama for Linux...")
        try:
            # Download and run the Ollama install script
            cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
            subprocess.run(cmd, shell=True, check=True)
            print("✅ Ollama installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama via script")
            return False
    
    elif system == "darwin":  # macOS
        print("📥 Installing Ollama for macOS...")
        print("Please visit: https://ollama.ai/download")
        print("Download the macOS installer and run it.")
        print("Then come back and run this script again!")
        return False
    
    elif system == "windows":
        print("📥 Installing Ollama for Windows...")
        print("Please visit: https://ollama.ai/download")
        print("Download the Windows installer and run it.")
        print("Then come back and run this script again!")
        return False
    
    else:
        print(f"❌ Unsupported OS: {system}")
        print("Please visit https://ollama.ai for manual installation instructions.")
        return False

def start_ollama_service():
    """Start the Ollama service"""
    print("🚀 Starting Ollama service...")
    
    # Try to start Ollama in the background
    try:
        if platform.system().lower() == "linux":
            # On Linux, try to start as a service or background process
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # On other systems, just try to serve
            subprocess.Popen(['ollama', 'serve'])
        
        # Wait a moment for service to start
        time.sleep(3)
        
        # Check if service is running
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama service is running!")
                return True
        except:
            pass
        
        print("⚠️ Ollama service might not be running properly")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start Ollama service: {e}")
        return False

def download_model(model_name="llama2"):
    """Download a specific model"""
    print(f"📦 Downloading {model_name} model...")
    print("This might take a while depending on your internet connection...")
    
    try:
        # Use ollama pull to download the model
        result = subprocess.run(['ollama', 'pull', model_name], 
                              capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print(f"✅ {model_name} model downloaded successfully!")
            return True
        else:
            print(f"❌ Failed to download {model_name}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Download timed out. You can try again later.")
        return False
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def test_ollama():
    """Test if Ollama is working properly"""
    print("🧪 Testing Ollama...")
    
    try:
        # Test API endpoint
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print("✅ Ollama is working! Available models:")
                for model in models[:3]:  # Show first 3 models
                    print(f"  - {model['name']}")
                return True
            else:
                print("⚠️ Ollama is running but no models are available")
                return False
        else:
            print("❌ Ollama API not responding properly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def show_alternative_options():
    """Show users alternative options if Ollama setup fails"""
    print("\n" + "="*50)
    print("🔄 Alternative Options:")
    print("="*50)
    print("1. 🤖 Hugging Face Models (No setup required)")
    print("   - The app will automatically use free Hugging Face models")
    print("   - Slower but requires no additional setup")
    print("   - Just run the app and it will work!")
    
    print("\n2. 🐳 Docker Ollama (If you have Docker)")
    print("   docker run -d -p 11434:11434 ollama/ollama")
    print("   docker exec -it <container> ollama pull llama2")
    
    print("\n3. 🌐 Manual Ollama Installation")
    print("   Visit: https://ollama.ai")
    print("   Download and install manually")
    
    print("\n4. ☁️ Cloud Options")
    print("   - Google Colab with Ollama")
    print("   - GitHub Codespaces")
    print("   - Any cloud VM with Ollama")

def main():
    """Main setup function"""
    print("🤖 AI Interview System - Ollama Setup")
    print("="*50)
    print("This script will help you set up Ollama for FREE AI interviews!")
    print("Ollama provides the best experience with local, private AI models.")
    print()
    
    # Step 1: Check if Ollama is installed
    if not check_ollama_installation():
        # Step 2: Install Ollama
        if not install_ollama():
            show_alternative_options()
            return
    
    # Step 3: Start Ollama service
    if not start_ollama_service():
        print("⚠️ Please start Ollama manually by running: ollama serve")
        print("Then run this script again to download models.")
        return
    
    # Step 4: Download recommended model
    print("\n📚 Recommended Models:")
    print("1. llama2 (7B) - Good balance of speed and quality")
    print("2. llama2:13b - Better quality, slower")
    print("3. codellama - Best for technical interviews")
    print("4. mistral - Fast and efficient")
    
    model_choice = input("\nWhich model would you like? (default: llama2): ").strip()
    if not model_choice:
        model_choice = "llama2"
    
    if download_model(model_choice):
        # Step 5: Test everything
        if test_ollama():
            print("\n🎉 SUCCESS! Ollama is ready for AI interviews!")
            print("\n🚀 Next steps:")
            print("1. Make sure .env file is configured (should be automatic)")
            print("2. Run the interview app: python run_app.py")
            print("3. Enjoy FREE, private AI interviews!")
        else:
            print("⚠️ Setup completed but testing failed. The app might still work.")
    else:
        print("⚠️ Model download failed. You can try again later.")
    
    show_alternative_options()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        show_alternative_options()