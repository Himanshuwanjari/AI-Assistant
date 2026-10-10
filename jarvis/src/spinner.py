# src/spinner.py
import sys
import threading
import time
from contextlib import contextmanager


@contextmanager
def thinking(message: str = "JARVIS is thinking"):
    """
    Show an animated spinner while the enclosed block runs.

    Usage:
        with thinking("JARVIS is thinking"):
            reply = jarvis.respond(user_input)
    """
    stop_event = threading.Event()

    def spin():
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while not stop_event.is_set():
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{frame} {message}...")
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
        # Clear the spinner line
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()