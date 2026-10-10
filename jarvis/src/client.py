# src/client.py
from google import genai
from src.config import GEMINI_API_KEY, DEFAULT_MODEL
from src.prompts import SYSTEM_PROMPT


class GeminiClient:
    """Wrapper around Google's Gemini Interactions API."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.last_interaction_id = None

    def chat(self, user_message: str) -> str:
        """Send a user message and return the assistant's reply."""
        kwargs = {
            "model": self.model,
            "input": user_message,
            "system_instruction": SYSTEM_PROMPT,
            "generation_config": {
                "thinking_level": "low", 
                "temperature": 0.7,
                "max_output_tokens": 2048,
            },
        }

        if self.last_interaction_id:
            kwargs["previous_interaction_id"] = self.last_interaction_id

        interaction = self.client.interactions.create(**kwargs)
        self.last_interaction_id = interaction.id

        # Access the text — try .output_text first, fall back to .outputs
        return interaction.output_text

    def reset(self):
        self.last_interaction_id = None

    def chat_stream(self, user_message: str):
        kwargs = {
            "model": self.model,
            "input": user_message,
            "system_instruction": SYSTEM_PROMPT,
            "generation_config": {
                "thinking_level": "low",
                "max_output_tokens": 1024,
            },
        }
        if self.last_interaction_id:
            kwargs["previous_interaction_id"] = self.last_interaction_id

        stream = self.client.interactions.create(**kwargs, stream=True)
        for chunk in stream:
            if getattr(chunk, "output_text", None):
                yield chunk.output_text