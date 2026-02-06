"""
Context Analyzer Module
Uses LLM APIs (Gemini, Groq, or OpenAI) to analyze screen text and extract meaningful context.
Supports multiple FREE providers!
"""

import os
import threading
import time
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from collections import deque

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


class LLMProvider:
    """Base class for LLM providers."""
    
    def analyze(self, prompt: str) -> str:
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Google Gemini API provider (FREE tier available)."""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your-gemini-api-key-here':
            raise ValueError("GEMINI_API_KEY not set in .env file")
        
        # Use google-genai library
        from google import genai
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = 'gemini-2.0-flash'
        print("[LLM] Using Google Gemini (FREE)")
    
    def analyze(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text


class GroqProvider(LLMProvider):
    """Groq API provider (FREE tier available)."""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key or self.api_key == 'your-groq-api-key-here':
            raise ValueError("GROQ_API_KEY not set in .env file")
        
        from groq import Groq
        self.client = Groq(api_key=self.api_key)
        print("[LLM] Using Groq (FREE)")
    
    def analyze(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, fast, and capable
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes screen content to help users with memory difficulties remember what they were doing. Be concise and accurate. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (paid)."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key or self.api_key == 'your-openai-api-key-here':
            raise ValueError("OPENAI_API_KEY not set in .env file")
        
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
        print("[LLM] Using OpenAI (paid)")
    
    def analyze(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes screen content to help users with memory difficulties remember what they were doing. Be concise and accurate. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content


def get_llm_provider() -> LLMProvider:
    """Get the configured LLM provider."""
    provider_name = os.getenv('LLM_PROVIDER', 'gemini').lower()
    
    providers = {
        'gemini': GeminiProvider,
        'groq': GroqProvider,
        'openai': OpenAIProvider
    }
    
    if provider_name not in providers:
        print(f"[LLM] Unknown provider '{provider_name}', defaulting to Gemini")
        provider_name = 'gemini'
    
    try:
        return providers[provider_name]()
    except Exception as e:
        print(f"[LLM] Failed to initialize {provider_name}: {e}")
        # Try fallback providers
        for fallback in ['gemini', 'groq', 'openai']:
            if fallback != provider_name:
                try:
                    print(f"[LLM] Trying fallback: {fallback}")
                    return providers[fallback]()
                except:
                    continue
        raise ValueError("No LLM provider could be initialized. Please check your .env file.")


class ContextAnalyzer:
    """
    Analyzes extracted text using LLM to understand user context and extract key information.
    """
    
    def __init__(self, analysis_interval: float = 10.0, max_history: int = 50):
        """
        Initialize the context analyzer.
        
        Args:
            analysis_interval: Seconds between LLM analysis calls
            max_history: Maximum number of key events to store
        """
        self.analysis_interval = analysis_interval
        self.max_history = max_history
        
        # LLM provider (lazy initialization)
        self._provider: Optional[LLMProvider] = None
        
        # Current context state
        self.current_activity: str = "Starting up..."
        self.current_app: str = "Unknown"
        self.key_events: deque = deque(maxlen=max_history)
        
        # Thread control
        self._running = False
        self._analysis_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Text callback - will be set by main app
        self._get_text_callback = None
        
        # Last analysis timestamp
        self._last_analysis_time = None
    
    def _get_provider(self) -> LLMProvider:
        """Get or create the LLM provider."""
        if self._provider is None:
            self._provider = get_llm_provider()
        return self._provider
    
    def set_text_callback(self, callback):
        """
        Set callback function to get recent text for analysis.
        Callback should return a string of recent screen text.
        """
        self._get_text_callback = callback
    
    def start(self):
        """Start the periodic analysis thread."""
        if self._running:
            return
        
        self._running = True
        self._analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self._analysis_thread.start()
        print("[ContextAnalyzer] Started periodic analysis")
    
    def stop(self):
        """Stop the analysis thread."""
        self._running = False
        if self._analysis_thread:
            self._analysis_thread.join(timeout=2.0)
            self._analysis_thread = None
        print("[ContextAnalyzer] Stopped analysis")
    
    def _analysis_loop(self):
        """Main analysis loop running periodically."""
        while self._running:
            try:
                if self._get_text_callback:
                    text = self._get_text_callback()
                    if text and text.strip():
                        self._analyze_text(text)
            except Exception as e:
                print(f"[ContextAnalyzer] Analysis error: {e}")
            
            # Wait for next analysis interval
            time.sleep(self.analysis_interval)
    
    def _analyze_text(self, text: str):
        """
        Analyze text using LLM to extract context and key information.
        
        Args:
            text: Screen text to analyze
        """
        try:
            provider = self._get_provider()
            
            # Truncate text if too long
            max_text_length = 4000
            if len(text) > max_text_length:
                text = text[:max_text_length] + "..."
            
            # Create the analysis prompt
            prompt = f"""Analyze the following screen text captured from a user's computer and extract:

1. ACTIVITY: What is the user currently doing? (e.g., "writing an email", "browsing Reddit", "coding in VS Code")
2. APPLICATION: What application or website are they using? (e.g., "Gmail", "Chrome - Reddit", "Visual Studio Code")
3. KEY_INFO: Extract any important information that the user might need to remember, such as:
   - OTP codes or verification codes
   - Phone numbers
   - Email addresses
   - Names of people or companies
   - URLs or links
   - Prices or amounts
   - Dates or times
   - Order numbers or tracking numbers
   - Any other critical information

Screen text:
---
{text}
---

Respond in the following JSON format only (no markdown, no extra text):
{{
    "activity": "brief description of what user is doing",
    "application": "name of app or website",
    "key_info": [
        {{"type": "otp", "value": "123456", "context": "from Gmail"}},
        {{"type": "email", "value": "person@example.com", "context": "sender"}},
        {{"type": "name", "value": "John Smith", "context": "contact name"}}
    ]
}}

If no key information is found, return an empty array for key_info.
Only include key_info items that are clearly important - don't include generic UI text."""

            result_text = provider.analyze(prompt)
            
            # Clean up the response if needed
            result_text = result_text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            
            # Update current state
            with self._lock:
                self.current_activity = result.get('activity', self.current_activity)
                self.current_app = result.get('application', self.current_app)
                
                # Add new key info to events
                key_info = result.get('key_info', [])
                timestamp = datetime.now()
                
                for info in key_info:
                    # Check for duplicates
                    is_duplicate = False
                    for existing in self.key_events:
                        if (existing['type'] == info.get('type') and 
                            existing['value'] == info.get('value')):
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        self.key_events.append({
                            'timestamp': timestamp,
                            'type': info.get('type', 'info'),
                            'value': info.get('value', ''),
                            'context': info.get('context', '')
                        })
            
            self._last_analysis_time = datetime.now()
            print(f"[ContextAnalyzer] Updated: {self.current_activity} in {self.current_app}")
            
        except json.JSONDecodeError as e:
            print(f"[ContextAnalyzer] JSON parse error: {e}")
        except Exception as e:
            print(f"[ContextAnalyzer] LLM error: {e}")
    
    def get_current_context(self) -> Dict[str, Any]:
        """
        Get the current context summary.
        
        Returns:
            Dictionary with activity, app, and key events
        """
        with self._lock:
            return {
                'activity': self.current_activity,
                'application': self.current_app,
                'key_events': list(self.key_events),
                'last_analysis': self._last_analysis_time
            }
    
    def get_recent_key_events(self, minutes: float = 5) -> List[Dict]:
        """
        Get key events from the last N minutes.
        
        Args:
            minutes: Number of minutes to look back
            
        Returns:
            List of key event dictionaries
        """
        cutoff = datetime.now().timestamp() - (minutes * 60)
        
        with self._lock:
            return [
                event for event in self.key_events
                if event['timestamp'].timestamp() >= cutoff
            ]
    
    def force_analyze(self, text: str) -> Dict[str, Any]:
        """
        Force an immediate analysis of the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Current context after analysis
        """
        self._analyze_text(text)
        return self.get_current_context()


# Test function
if __name__ == "__main__":
    print("Testing Context Analyzer Module...")
    print()
    
    # Load .env
    load_dotenv()
    
    # Check which provider is configured
    provider = os.getenv('LLM_PROVIDER', 'gemini')
    print(f"Configured provider: {provider}")
    
    # Test with sample text
    sample_text = """
    Gmail - Inbox
    From: John Smith <john.smith@company.com>
    Subject: Your verification code
    
    Hi there,
    
    Your verification code is: 847291
    
    This code expires in 10 minutes.
    
    Best regards,
    Security Team
    
    Reply Forward
    """
    
    try:
        analyzer = ContextAnalyzer()
        
        # Force immediate analysis
        result = analyzer.force_analyze(sample_text)
        
        print(f"Activity: {result['activity']}")
        print(f"Application: {result['application']}")
        print(f"Key Events: {result['key_events']}")
        print("Test complete!")
    except Exception as e:
        print(f"Test failed: {e}")
        print("Make sure you have set up your API key in the .env file")
