# src/voice.py
"""
Voice input for JARVIS — silence-based streaming recorder.

Listens continuously, stops after SILENCE_SECONDS of quiet,
then transcribes with Google Web Speech (free, no API key).
"""

import io
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr


class VoiceInputError(Exception):
    """Recoverable voice input failure."""
    pass


class VoiceInput:
    def __init__(
        self,
        language: str = "en-IN",
        sample_rate: int = 16000,
        silence_seconds: float = 2.0,     # stop after this much quiet
        max_seconds: float = 30.0,        # hard safety cap
        min_seconds: float = 0.6,         # ignore ultra-short blips
    ):
        self.language = language
        self.sample_rate = sample_rate
        self.silence_seconds = silence_seconds
        self.max_seconds = max_seconds
        self.min_seconds = min_seconds
        self.recognizer = sr.Recognizer()

    def _calibrate(self) -> float:
        """Sample 0.5s of ambient noise → set speech threshold."""
        rec = sd.rec(
            int(0.5 * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()
        rms = float(np.sqrt(np.mean(rec.astype(np.float32) ** 2)))
        return max(rms * 4.0, 250.0)

    def listen(self) -> str:
        threshold = self._calibrate()

        chunk = 1024
        chunk_sec = chunk / self.sample_rate
        silence_chunks_needed = int(self.silence_seconds / chunk_sec)
        max_chunks = int(self.max_seconds / chunk_sec)
        min_chunks = int(self.min_seconds / chunk_sec)

        frames = []
        state = {"silent": 0, "spoken": False, "stop": False}

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy())
            rms = float(np.sqrt(np.mean(indata.astype(np.float32) ** 2)))

            if rms > threshold:
                state["spoken"] = True
                state["silent"] = 0
            elif state["spoken"]:
                state["silent"] += 1

            if len(frames) >= max_chunks:
                state["stop"] = True
            elif (
                state["spoken"]
                and state["silent"] >= silence_chunks_needed
                and len(frames) >= min_chunks
            ):
                state["stop"] = True

        try:
            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=chunk,
                callback=callback,
            )
            stream.start()
        except Exception as e:
            raise VoiceInputError(f"Could not open microphone: {e}") from e

        try:
            while not state["stop"]:
                sd.sleep(50)
        finally:
            stream.stop()
            stream.close()

        if not state["spoken"]:
            raise VoiceInputError("No speech detected.")
        if not frames:
            raise VoiceInputError("No audio captured.")

        audio = np.concatenate(frames, axis=0)

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio.tobytes())

        audio_data = sr.AudioData(buf.getvalue(), self.sample_rate, 2)

        try:
            text = self.recognizer.recognize_google(
                audio_data, language=self.language
            )
        except sr.UnknownValueError:
            raise VoiceInputError("Could not understand the audio.") from None
        except sr.RequestError as e:
            raise VoiceInputError(f"Speech service unreachable: {e}") from e

        text = text.strip()
        if not text:
            raise VoiceInputError("Empty transcription.")
        return text