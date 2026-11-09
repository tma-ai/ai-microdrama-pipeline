"""Transcribe one or more media files with faster-whisper medium.en (CPU int8). Usage: transcribe.py file [file...]"""
import os, subprocess, sys
import numpy as np
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from faster_whisper import WhisperModel

m = WhisperModel("medium.en", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(audio, word_timestamps=True)
    print("==", os.path.basename(f), round(len(audio) / 16000, 1), "s")
    for s in segs:
        print(f"  {s.start:5.2f}-{s.end:5.2f}  {s.text.strip()}")
