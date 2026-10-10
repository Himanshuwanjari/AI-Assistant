# run.py
import sys
from src.jarvis import Jarvis
from src.spinner import status, prompt, C
from src.voice import VoiceInput, VoiceInputError


BANNER = """
╔══════════════════════════════════════════╗
║          J A R V I S   V 2               ║
║   Personal AI Assistant — Google Gemini  ║
║   Type 'exit'/'quit' to stop             ║
║   Type 'reset' to clear conversation     ║
║   Type 'v' to speak instead of typing    ║
╚══════════════════════════════════════════╝
"""


def get_voice_input(voice: VoiceInput) -> str | None:
    """Listen → show transcription → confirm / edit / cancel."""
    try:
        with status("listening"):
            text = voice.listen()
    except VoiceInputError as e:
        print(f"\n{C.RED}[Voice] {e}{C.RESET}")
        return None

    print(f"\n{C.BOLD}📝 Heard:{C.RESET} {text}")

    choice = prompt("Send? [Y/n/edit]: ").strip().lower()

    if choice in ("", "y", "yes"):
        return text
    if choice in ("n", "no"):
        print(f"{C.DIM}Cancelled.{C.RESET}")
        return None
    if choice == "edit":
        edited = prompt("Edit: ").strip()
        return edited if edited else None
    return text


def main():
    print(BANNER)
    jarvis = Jarvis()
    voice = VoiceInput()

    while True:
        try:
            user_input = input(f"\n{C.CYAN}You:{C.RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.GREEN}JARVIS: Goodbye.{C.RESET}")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(f"{C.GREEN}JARVIS: Goodbye.{C.RESET}")
            break

        if user_input.lower() == "reset":
            jarvis.reset()
            print(f"{C.YELLOW}JARVIS: Conversation cleared.{C.RESET}")
            continue

        if user_input.lower() == "v":
            user_input = get_voice_input(voice)
            if user_input is None:
                continue

        try:
            with status("sending"):
                reply = jarvis.respond(user_input)
            print(f"\n{C.GREEN}{C.BOLD}JARVIS:{C.RESET} {reply}")
        except Exception as e:
            print(f"\n{C.RED}[Error] {e}{C.RESET}")


if __name__ == "__main__":
    main()