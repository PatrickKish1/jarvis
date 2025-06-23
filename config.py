import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Voice Settings
VOICE_SETTINGS = {
    'voice': 'com.apple.speech.synthesis.voice.evan',
    'rate': 170,
    'volume': 1.0
}

# Speech Recognition Settings
RECOGNITION_SETTINGS = {
    'energy_threshold': 200,
    'dynamic_energy_threshold': False,
    'pause_threshold': 0.7,
    'operation_timeout': None
}

# OpenAI Settings
OPENAI_SETTINGS = {
    'model': 'gpt-4o-mini',
    'max_tokens': 200,
    'temperature': 0.7
}

# Perplexity Settings
PERPLEXITY_SETTINGS = {
    'model': 'sonar',
    'max_tokens': 200,
    'temperature': 0.3,
    'timeout': 10
}

# System Prompt
SYSTEM_PROMPT = """You are Jarvis, a witty, efficient AI assistant inspired by Iron Man's AI. 
Respond concisely and helpfully. Use a formal but friendly tone. 
Prefer available functions (time, calculator, web search, URL open). 
If a request is unsupported, briefly explain what you can do instead.""" 