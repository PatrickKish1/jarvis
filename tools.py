import datetime
import webbrowser
import requests
import platform
import psutil
import os
from config import PERPLEXITY_API_KEY, PERPLEXITY_SETTINGS
from desktop_agent import DesktopAgent

# Initialize desktop agent
desktop_agent = DesktopAgent()

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

def open_application(app_name):
    """Open an application by name."""
    return desktop_agent.open_application(app_name)

def take_screenshot(filename=None):
    """Take a screenshot of the entire screen."""
    return desktop_agent.take_screenshot(filename)

def click_position(x, y):
    """Click at specific coordinates."""
    return desktop_agent.click_position(x, y)

def type_text(text):
    """Type text at current cursor position."""
    return desktop_agent.type_text(text)

def press_key(key):
    """Press a specific key."""
    return desktop_agent.press_key(key)

def get_screen_size():
    """Get screen dimensions."""
    return desktop_agent.get_screen_size()

def get_mouse_position():
    """Get current mouse position."""
    return desktop_agent.get_mouse_position()

def scroll(direction, amount=3):
    """Scroll up or down."""
    return desktop_agent.scroll(direction, amount)

def close_active_window():
    """Close the currently active window."""
    return desktop_agent.close_active_window()

def minimize_window():
    """Minimize the currently active window."""
    return desktop_agent.minimize_window()

def get_running_apps():
    """Get list of currently running applications."""
    return desktop_agent.get_running_apps()

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    return desktop_agent.copy_to_clipboard(text)

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
        "name": "open_application",
        "description": "Open an application by name (e.g., chrome, safari, terminal, calculator, spotify, mail, messages, photos, music, notes, calendar, reminders, maps, weather, clock, settings).",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "The name of the application to open"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "take_screenshot",
        "description": "Take a screenshot of the entire screen.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Optional filename for the screenshot"}
            },
            "required": []
        }
    },
    {
        "name": "click_position",
        "description": "Click at specific screen coordinates.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X coordinate"},
                "y": {"type": "integer", "description": "Y coordinate"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "type_text",
        "description": "Type text at the current cursor position.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to type"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "press_key",
        "description": "Press a specific key (e.g., enter, space, tab, escape, backspace, delete, up, down, left, right).",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to press"}
            },
            "required": ["key"]
        }
    },
    {
        "name": "get_screen_size",
        "description": "Get the screen dimensions in pixels.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "get_mouse_position",
        "description": "Get the current mouse cursor position.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "scroll",
        "description": "Scroll up or down on the current page.",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "description": "Scroll direction: 'up' or 'down'"},
                "amount": {"type": "integer", "description": "Number of scroll units (default: 3)"}
            },
            "required": ["direction"]
        }
    },
    {
        "name": "close_active_window",
        "description": "Close the currently active window.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "minimize_window",
        "description": "Minimize the currently active window.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "get_running_apps",
        "description": "Get a list of currently running applications.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "copy_to_clipboard",
        "description": "Copy text to the system clipboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to copy to clipboard"}
            },
            "required": ["text"]
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
    "get_system_stats": get_system_stats,
    "open_application": open_application,
    "take_screenshot": take_screenshot,
    "click_position": click_position,
    "type_text": type_text,
    "press_key": press_key,
    "get_screen_size": get_screen_size,
    "get_mouse_position": get_mouse_position,
    "scroll": scroll,
    "close_active_window": close_active_window,
    "minimize_window": minimize_window,
    "get_running_apps": get_running_apps,
    "copy_to_clipboard": copy_to_clipboard,
    "get_web_data": get_web_data
} 