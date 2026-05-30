import os
import subprocess
import sys

def play_audio(filepath):
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filepath])

def review_clips(input_dir):
    wav_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".wav")])
    total = len(wav_files)
    kept = 0
    deleted = 0

    for i, filename in enumerate(wav_files):
        filepath = os.path.join(input_dir, filename)
        while True:
            print(f"\n[{i+1}/{total}] kept:{kept} deleted:{deleted} | {filename}")
            print("Playing...")
            play_audio(filepath)
            print("[Enter]=delete  [s]=keep  [r]=replay  [q]=quit")
            key = input("Choice: ").strip().lower()

            if key == "r":
                continue
            elif key == "" :
                os.remove(filepath)
                deleted += 1
                print("Deleted.")
                break
            elif key == "s":
                kept += 1
                print("Kept.")
                break
            elif key == "q":
                print(f"Done. kept:{kept} deleted:{deleted}")
                sys.exit(0)
            else:
                print("Invalid key, try again.")

    print(f"\nFinished. kept:{kept} deleted:{deleted}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder of wav clips to review")
    args = parser.parse_args()
    review_clips(args.input)
