# src/spinner.py
import sys
import threading
import time
from contextlib import contextmanager


class C:
    RESET   = "\033[0m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    MAGENTA = "\033[35m"
    RED     = "\033[31m"
    BOLD    = "\033[1m"


STATES = {
    "listening":  ("🎤", "Listening",          C.CYAN),
    "thinking":   ("🧠", "JARVIS is thinking", C.MAGENTA),
    "correcting": ("✏️", "Waiting for edit",   C.YELLOW),
    "speaking":   ("🔊", "Speaking",           C.GREEN),
    "sending":    ("📡", "Sending to Gemini",  C.MAGENTA),
    "error":      ("⚠️", "Error",              C.RED),
}


@contextmanager
def status(state: str = "thinking", message: str | None = None):
    """Animated spinner for blocking operations (no user input inside)."""
    icon, default_msg, color = STATES.get(state, ("•", state, C.RESET))
    msg = message or default_msg

    stop_event = threading.Event()
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def spin():
        i = 0
        while not stop_event.is_set():
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{color}{frame} {icon}  {msg}...{C.RESET}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.08)

    thread = threading.Thread(target=spin, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop_event.set()
        thread.join()
        sys.stdout.write("\r" + " " * (len(msg) + 12) + "\r")
        sys.stdout.flush()


def prompt(text: str, state: str = "correcting") -> str:
    """
    Static, colored prompt for interactive input().
    Use INSTEAD of wrapping input() in a spinner.
    """
    icon, _, color = STATES.get(state, ("•", "", C.RESET))
    sys.stdout.write(f"{color}{icon}  {text}{C.RESET}")
    sys.stdout.flush()
    return input()


# Backwards-compatible alias
thinking = status