# src/jarvis.py
from src.client import GeminiClient


class Jarvis:
    def __init__(self):
        self.client = GeminiClient()

    def respond(self, user_input: str) -> str:
        """Send user input and return JARVIS's reply."""
        return self.client.chat(user_input)

    def reset(self):
        """Clear conversation history."""
        self.client.reset()