#!/usr/bin/env python3
"""
Setup script for AI Revision Agent
Handles installation and initial configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🤖 AI Revision Agent - Setup Script")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("\n🔑 Setting up environment file...")
        with open(env_file, "w") as f:
            f.write("# OpenRouter API Configuration\n")
            f.write("OPENROUTER_API_KEY=your_openrouter_api_key_here\n\n")
            f.write("# Optional: Set your app name and URL for OpenRouter analytics\n")
            f.write("# OPENROUTER_HTTP_REFERER=your_app_name\n")
            f.write("# OPENROUTER_X_TITLE=AI Revision Agent\n")
        
        print("✅ Created .env file")
        print("⚠️  Please edit .env file and add your OpenRouter API key")
        print("   Get your key from: https://openrouter.ai/")
    else:
        print("✅ .env file already exists")

def run_tests():
    """Run the test suite to verify installation"""
    print("\n🧪 Running tests to verify installation...")
    try:
        result = subprocess.run([sys.executable, "3_Agent_Code/test_runner.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("🚀 Setup Complete! Usage Instructions:")
    print("=" * 60)
    print("\n1. Edit .env file and add your OpenRouter API key")
    print("\n2. Run the CLI version:")
    print("   python 3_Agent_Code/cli_interface.py")
    print("\n3. Run the web interface:")
    print("   streamlit run streamlit_app.py")
    print("\n4. Run tests anytime:")
    print("   python 3_Agent_Code/test_runner.py")
    print("\n📚 Happy studying!")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    setup_env_file()
    
    # Run tests (optional, may fail without API key)
    print("\n🔍 Testing installation (may fail without API key)...")
    run_tests()
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    main()