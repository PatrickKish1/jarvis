import subprocess
import os
import platform
import pyautogui
import time
from PIL import Image
import psutil

class DesktopAgent:
    def __init__(self):
        self.system = platform.system()
        # Set pyautogui safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def open_application(self, app_name):
        """Open an application by name."""
        try:
            if self.system == "Darwin":  # macOS
                # Common macOS apps
                app_mapping = {
                    "chrome": "Google Chrome",
                    "safari": "Safari",
                    "firefox": "Firefox",
                    "spotify": "Spotify",
                    "terminal": "Terminal",
                    "finder": "Finder",
                    "mail": "Mail",
                    "messages": "Messages",
                    "facetime": "FaceTime",
                    "photos": "Photos",
                    "music": "Music",
                    "calculator": "Calculator",
                    "notes": "Notes",
                    "calendar": "Calendar",
                    "reminders": "Reminders",
                    "maps": "Maps",
                    "weather": "Weather",
                    "clock": "Clock",
                    "settings": "System Preferences",
                    "preferences": "System Preferences"
                }
                
                app_name_lower = app_name.lower()
                actual_app_name = app_mapping.get(app_name_lower, app_name)
                
                subprocess.run(["open", "-a", actual_app_name])
                return f"Opened {actual_app_name}"
                
            elif self.system == "Windows":
                # Common Windows apps
                app_mapping = {
                    "chrome": "chrome.exe",
                    "edge": "msedge.exe",
                    "firefox": "firefox.exe",
                    "notepad": "notepad.exe",
                    "calculator": "calc.exe",
                    "explorer": "explorer.exe",
                    "cmd": "cmd.exe",
                    "powershell": "powershell.exe"
                }
                
                app_name_lower = app_name.lower()
                actual_app_name = app_mapping.get(app_name_lower, app_name)
                
                subprocess.Popen(actual_app_name)
                return f"Opened {actual_app_name}"
                
            elif self.system == "Linux":
                # Common Linux apps
                app_mapping = {
                    "chrome": "google-chrome",
                    "firefox": "firefox",
                    "terminal": "gnome-terminal",
                    "calculator": "gnome-calculator",
                    "files": "nautilus",
                    "gedit": "gedit"
                }
                
                app_name_lower = app_name.lower()
                actual_app_name = app_mapping.get(app_name_lower, app_name)
                
                subprocess.Popen([actual_app_name])
                return f"Opened {actual_app_name}"
                
        except Exception as e:
            return f"Could not open {app_name}: {str(e)}"
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the entire screen."""
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Could not take screenshot: {str(e)}"
    
    def click_position(self, x, y):
        """Click at specific coordinates."""
        try:
            pyautogui.click(x, y)
            return f"Clicked at position ({x}, {y})"
        except Exception as e:
            return f"Could not click at position ({x}, {y}): {str(e)}"
    
    def type_text(self, text):
        """Type text at current cursor position."""
        try:
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        except Exception as e:
            return f"Could not type text: {str(e)}"
    
    def press_key(self, key):
        """Press a specific key."""
        try:
            pyautogui.press(key)
            return f"Pressed key: {key}"
        except Exception as e:
            return f"Could not press key {key}: {str(e)}"
    
    def get_screen_size(self):
        """Get screen dimensions."""
        try:
            width, height = pyautogui.size()
            return f"Screen size: {width}x{height} pixels"
        except Exception as e:
            return f"Could not get screen size: {str(e)}"
    
    def get_mouse_position(self):
        """Get current mouse position."""
        try:
            x, y = pyautogui.position()
            return f"Mouse position: ({x}, {y})"
        except Exception as e:
            return f"Could not get mouse position: {str(e)}"
    
    def scroll(self, direction, amount=3):
        """Scroll up or down."""
        try:
            if direction.lower() in ["up", "scrollup"]:
                pyautogui.scroll(amount)
                return f"Scrolled up {amount} units"
            elif direction.lower() in ["down", "scrolldown"]:
                pyautogui.scroll(-amount)
                return f"Scrolled down {amount} units"
            else:
                return "Invalid scroll direction. Use 'up' or 'down'"
        except Exception as e:
            return f"Could not scroll: {str(e)}"
    
    def close_active_window(self):
        """Close the currently active window."""
        try:
            if self.system == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'w')
            elif self.system == "Windows":
                pyautogui.hotkey('alt', 'f4')
            elif self.system == "Linux":
                pyautogui.hotkey('ctrl', 'w')
            return "Closed active window"
        except Exception as e:
            return f"Could not close window: {str(e)}"
    
    def minimize_window(self):
        """Minimize the currently active window."""
        try:
            if self.system == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'm')
            elif self.system == "Windows":
                pyautogui.hotkey('win', 'down')
            elif self.system == "Linux":
                pyautogui.hotkey('ctrl', 'super', 'down')
            return "Minimized active window"
        except Exception as e:
            return f"Could not minimize window: {str(e)}"
    
    def get_running_apps(self):
        """Get list of currently running applications."""
        try:
            running_apps = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    running_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Get unique apps and limit to top 10
            unique_apps = list(set(running_apps))[:10]
            return f"Running apps: {', '.join(unique_apps)}"
        except Exception as e:
            return f"Could not get running apps: {str(e)}"
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            pyautogui.write(text)
            if self.system == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'a')  # Select all
                pyautogui.hotkey('cmd', 'c')  # Copy
            elif self.system == "Windows":
                pyautogui.hotkey('ctrl', 'a')  # Select all
                pyautogui.hotkey('ctrl', 'c')  # Copy
            elif self.system == "Linux":
                pyautogui.hotkey('ctrl', 'a')  # Select all
                pyautogui.hotkey('ctrl', 'c')  # Copy
            return f"Copied '{text}' to clipboard"
        except Exception as e:
            return f"Could not copy to clipboard: {str(e)}" 