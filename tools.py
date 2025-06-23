import datetime
import webbrowser
import requests
from config import PERPLEXITY_API_KEY, PERPLEXITY_SETTINGS

def get_current_time():
    """Get the current system time."""
    return datetime.datetime.now().strftime("%I:%M %p")

def open_any_url(url):
    """Opens any URL in the browser."""
    try:
        webbrowser.open(url)
        return f"Opening {url} in your browser."
    except Exception as e:
        return f"Sorry, I couldn't open {url}. Error: {str(e)}"

def simple_calculator(expression):
    """Evaluate a basic math expression."""
    try:
        # Remove any potentially dangerous characters
        safe_expression = ''.join(c for c in expression if c.isdigit() or c in '+-*/.() ')
        result = eval(safe_expression)
        return f"The result of {expression} is {result}."
    except Exception as e:
        return f"Sorry, I couldn't compute that expression: {expression}"

def get_web_data(query):
    """Fetch real-time web data about a topic or question using Perplexity API."""
    if not PERPLEXITY_API_KEY:
        return "Sorry, I don't have access to web search at the moment."
    
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": PERPLEXITY_SETTINGS['model'],
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide only the final answer. Do not include explanations. Provide a list if needed with a short intro."
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "max_tokens": PERPLEXITY_SETTINGS['max_tokens'],
            "temperature": PERPLEXITY_SETTINGS['temperature']
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=PERPLEXITY_SETTINGS['timeout']
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Sorry, I couldn't fetch web data for that query."
            
    except Exception as e:
        return f"Sorry, I encountered an error while searching the web: {str(e)}"

# Function definitions for OpenAI
FUNCTIONS = [
    {
        "name": "get_current_time",
        "description": "Get the current system time.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "open_any_url",
        "description": "Opens any URL in the browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to open"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "simple_calculator",
        "description": "Evaluate a basic math expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The mathematical expression to evaluate"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_web_data",
        "description": "Fetch real-time web data about a topic or question (especially post-2020 events, news, or anything involving today, recent, or this week).",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query or question to search the web for"}
            },
            "required": ["query"]
        }
    }
]

# Function mapping for easy lookup
FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "open_any_url": open_any_url,
    "simple_calculator": simple_calculator,
    "get_web_data": get_web_data
} 