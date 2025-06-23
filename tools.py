import datetime
import webbrowser
import requests
import platform
import psutil
import os
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

def get_system_stats():
    """Get comprehensive system specifications and statistics."""
    try:
        stats = []
        
        # OS Information
        stats.append(f"OS: {platform.system()} {platform.release()}")
        stats.append(f"Architecture: {platform.machine()}")
        stats.append(f"Python Version: {platform.python_version()}")
        
        # CPU Information
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        stats.append(f"CPU: {cpu_count} cores, {cpu_percent}% usage")
        
        # Memory Information
        memory = psutil.virtual_memory()
        memory_total = memory.total / (1024**3)  # Convert to GB
        memory_used = memory.used / (1024**3)
        memory_percent = memory.percent
        stats.append(f"Memory: {memory_used:.1f}GB used of {memory_total:.1f}GB ({memory_percent}%)")
        
        # Disk Information
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024**3)  # Convert to GB
        disk_used = disk.used / (1024**3)
        disk_free = disk.free / (1024**3)
        disk_percent = (disk.used / disk.total) * 100
        stats.append(f"Disk: {disk_used:.1f}GB used, {disk_free:.1f}GB free of {disk_total:.1f}GB ({disk_percent:.1f}%)")
        
        # Network Information
        network = psutil.net_io_counters()
        bytes_sent = network.bytes_sent / (1024**2)  # Convert to MB
        bytes_recv = network.bytes_recv / (1024**2)
        stats.append(f"Network: {bytes_sent:.1f}MB sent, {bytes_recv:.1f}MB received")
        
        # Boot Time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        stats.append(f"Uptime: {uptime.days} days, {uptime.seconds // 3600} hours")
        
        # Process Count
        process_count = len(psutil.pids())
        stats.append(f"Processes: {process_count} running")
        
        return " | ".join(stats)
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve system stats: {str(e)}"

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
        "name": "get_system_stats",
        "description": "Get comprehensive system specifications and statistics including OS, CPU, memory, disk, network, and process information.",
        "parameters": {"type": "object", "properties": {}}
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
    "get_system_stats": get_system_stats,
    "get_web_data": get_web_data
} 