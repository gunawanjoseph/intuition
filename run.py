#!/usr/bin/env python3
"""
Memory Context Overlay - Launcher Script
Run this script to start the application.
"""

import sys
import os

# Ensure we're running from the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Installing python-dotenv...")
    os.system(f"{sys.executable} -m pip install python-dotenv --quiet")
    from dotenv import load_dotenv
    load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Check for API key based on provider
provider = os.environ.get('LLM_PROVIDER', 'gemini').lower()
key_map = {
    'gemini': 'GEMINI_API_KEY',
    'groq': 'GROQ_API_KEY', 
    'openai': 'OPENAI_API_KEY'
}

key_name = key_map.get(provider, 'GEMINI_API_KEY')
api_key = os.environ.get(key_name, '')

if not api_key or api_key.startswith('your-'):
    print("=" * 60)
    print("⚠️  API KEY NOT CONFIGURED!")
    print("=" * 60)
    print()
    print(f"You're using provider: {provider.upper()}")
    print(f"But {key_name} is not set in your .env file")
    print()
    
    if provider == 'gemini':
        print("🆓 GET YOUR FREE GEMINI API KEY:")
        print("   1. Go to: https://aistudio.google.com/apikey")
        print("   2. Click 'Create API Key'")
        print("   3. Copy the key")
        print("   4. Paste it in the .env file")
    elif provider == 'groq':
        print("🆓 GET YOUR FREE GROQ API KEY:")
        print("   1. Go to: https://console.groq.com/keys")
        print("   2. Create an account (no credit card needed)")
        print("   3. Create a new API key")
        print("   4. Paste it in the .env file")
    else:
        print("💳 GET YOUR OPENAI API KEY:")
        print("   1. Go to: https://platform.openai.com/api-keys")
        print("   2. Create a new secret key")
        print("   3. Paste it in the .env file")
    
    print()
    print("=" * 60)
    print()
    
    response = input("Continue anyway? (y/n): ").strip().lower()
    if response != 'y':
        print("Exiting. Please configure your .env file and try again.")
        sys.exit(0)

# Import and run main application
from main import main

if __name__ == "__main__":
    sys.exit(main())
