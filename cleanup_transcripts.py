import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Directory containing wav and transcript files")
args = parser.parse_args()

transcript_files = glob.glob(os.path.join(args.input, '*_transcripts.txt'))
total_kept = 0
total_lines = 0

for transcript_file in transcript_files:
    with open(transcript_file) as f:
        lines = f.readlines()

    kept = [l for l in lines if os.path.exists(os.path.join(args.input, l.split('|')[0].strip()))]

    # Safety check - don't wipe if nothing was kept
    if len(kept) == 0 and len(lines) > 0:
        print(f"{transcript_file}: SKIPPED - all lines would be removed, check paths")
        continue

    with open(transcript_file, 'w') as f:
        f.writelines(kept)
    total_kept += len(kept)
    total_lines += len(lines)
    print(f"{transcript_file}: kept {len(kept)} of {len(lines)}")

print(f"\nTotal: kept {total_kept} of {total_lines}")
