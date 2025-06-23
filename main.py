#!/usr/bin/env python3
"""
Jarvis - AI Voice Assistant
A modular voice assistant with speech recognition, AI processing, and function calling.
"""

from jarvis import Jarvis

def main():
    """Main entry point for the Jarvis application."""
    try:
        # Create and start Jarvis
        jarvis = Jarvis()
        jarvis.start()
    except KeyboardInterrupt:
        print("\nJarvis interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()