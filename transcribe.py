# To execute this script, run `python3 transcribe.py`
from faster_whisper import WhisperModel

model = WhisperModel("small", device="auto")  # Uses MPS (Apple Silicon GPU) if available
segments, info = model.transcribe("assets/task-manager/trimmed.mp4")

with open("assets/task-manager/transcript.txt", "w") as f:
    for segment in segments:
        start_min = int(segment.start // 60)
        start_sec = int(segment.start % 60)
        end_min = int(segment.end // 60)
        end_sec = int(segment.end % 60)
        f.write(f"{start_min:02}:{start_sec:02}-{end_min:02}:{end_sec:02}\n{segment.text.strip()}\n\n")
