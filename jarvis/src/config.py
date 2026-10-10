# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Create a .env file with GEMINI_API_KEY=your_key"
    )

DEFAULT_MODEL = "gemini-3.8-flash"
# DEFAULT_MODEL = "gemini-3.8-flash-lite"