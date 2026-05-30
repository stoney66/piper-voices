Custom Piper Voices created using demucs (htdemucs_ft), whisperx and TextyMcSpeechy

Jake the Dog from Adventure Time

Tom Servo from MST3K

Crow from MST3K

Joel from MST3K


Script usage

python3 extract_speaker.py --speaker SPEAKER_11 --episode MST3K_S03E21_trimmed --tag crow_s03e21 --output crow-s3

python3 review_clips.py --input speaker_clips/crow-s3/

python3 cleanup_transcripts.py --input speaker_clips/crow-s3/

mv speaker_clips/crow-s3/* speaker_clips/crow-complete/

cat speaker_clips/joel-complete/*_transcripts.txt > speaker_clips/joel-complete//metadata.csv
sed -i 's/\.wav|/|/' speaker_clips/joel-complete//metadata.csv


# check length all wav files dir walk
python3 -c "
import soundfile as sf
import os
total = 0
for root, dirs, files in os.walk('speaker_clips/crow-complete'):
    for f in files:
        if f.endswith('.wav'):
            info = sf.info(os.path.join(root, f))
            total += info.duration
print(f'Total: {total/60:.1f} minutes')
"

# check wav length
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 speaker_clips/crow-s3/crow_s03e20_0007.wav

# trim
ffmpeg -i speaker_clips/crow-s3/crow_s03e20_0007.wav -t 1.6 -c copy crow_s03e20_0007.wav
