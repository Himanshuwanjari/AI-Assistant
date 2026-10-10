# run.py
import sys
from src.jarvis import Jarvis
from src.spinner import thinking          # NEW


BANNER = """
╔══════════════════════════════════════════╗
║          J A R V I S   V 1               ║
║   Personal AI Assistant — Google Gemini  ║
║   Type 'exit' or 'quit' to stop          ║
║   Type 'reset' to clear conversation     ║
╚══════════════════════════════════════════╝
"""


def main():
    print(BANNER)
    jarvis = Jarvis()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nJARVIS: Goodbye.")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("JARVIS: Goodbye.")
            break

        if user_input.lower() == "reset":
            jarvis.reset()
            print("JARVIS: Conversation cleared.")
            continue

        try:
            with thinking("JARVIS is thinking"):     # NEW
                reply = jarvis.respond(user_input)   # NEW            
            print(f"\nJARVIS: {reply}")
        except Exception as e:
            print(f"\n[Error] {e}")


if __name__ == "__main__":
    main()