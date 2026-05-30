import json
import soundfile as sf
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--speaker", required=True, help="Speaker ID e.g. SPEAKER_02")
parser.add_argument("--episode", required=True, help="Episode name e.g. MST3K_S02E01")
parser.add_argument("--tag", required=True, help="Season/character tag e.g. servo_s02")
parser.add_argument("--output", required=True, help="Output subdirectory name e.g. tom_servo_clips")
parser.add_argument("--min_duration", type=float, default=1.0)
args = parser.parse_args()

JSON_FILE = f"whisperx_files/{args.episode}.json"
AUDIO_FILE = f"vocal_files/{args.episode}.wav"
OUTPUT_DIR = f"./speaker_clips/{args.output}"
TRANSCRIPT_FILE = os.path.join(OUTPUT_DIR, f"{args.tag}_transcripts.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(JSON_FILE) as f:
    data = json.load(f)

audio, sample_rate = sf.read(AUDIO_FILE)
min_samples = int(args.min_duration * sample_rate)
transcript_lines = []
count = 0

for seg in data["segments"]:
    if seg.get("speaker") != args.speaker:
        continue
    start = int(seg["start"] * sample_rate)
    end = int(seg["end"] * sample_rate)
    text = seg["text"].strip()
    if (end - start) < min_samples:
        continue
    clip = audio[start:end]
    filename = f"{args.tag}_{count:04d}.wav"
    sf.write(os.path.join(OUTPUT_DIR, filename), clip, sample_rate)
    transcript_lines.append(f"{filename}|{text}")
    count += 1

with open(TRANSCRIPT_FILE, "w") as f:
    f.write("\n".join(transcript_lines))

print(f"Extracted {count} clips to {OUTPUT_DIR}")
