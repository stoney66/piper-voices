Custom Piper Voices created using demucs (htdemucs_ft), whisperx and TextyMcSpeechy

Jake the Dog from Adventure Time
Tom Servo from MST3K
Crow from MST3K
Joel from MST3K


# Create venv
python3 -m venv venv
source venv/bin/activate

pip install ffmpeg
pip install whisperx

# Use demucs to grab vocals 

demucs --two-stems=vocals -n htdemucs_ft -o . "MST3K_S03E23.mp4"

or

for f in MST3K_S03E0*.mp4; do
    demucs --two-stems=vocals -n htdemucs_ft -o . "$f" && rm "htdemucs_ft/${f%.mp4}/no_vocals.wav"
done

# Trim first 130s (intro)
for f in vocal_files/MST3K_S03E1*.wav; do
    base=$(basename "$f" .wav)
    trimmed="vocal_files/${base}_trimmed.wav"
    if [[ "$base" != *_trimmed ]]; then
        echo "Trimming $f -> $trimmed"
        ffmpeg -i "$f" -ss 130 -c copy "$trimmed"
    fi
done

# Create whisperX files (json, txt)
for f in vocal_files/MST3K_S03E1*_trimmed.wav; do
    echo "Processing $f"
    whisperx "$f" --batch_size 2 \
      --model large-v2 --diarize \
      --hf_token <token> \
      --language en \
      --output_dir ./whisperx_files/
done

# cat whisperx_files/XXXXX txt file for the speakers and figure out which one is your Speaker while playing audio from same vocal_file


# Script usage

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


##### TextyMcSpeechy

mkdir -p ~/TextyMcSpeechy/tts_dojo/DATASETS/tom_servo

cd ~/TextyMcSpeechy/tts_dojo
./newdojo.sh tom_servo

cp /mnt/nas/voice_training/speaker_clips/servo-complete/*.wav ~/TextyMcSpeechy/tts_dojo/DATASETS/tom_servo/
cp /mnt/nas/voice_training/speaker_clips/servo-complete/metadata.csv ~/TextyMcSpeechy/tts_dojo/DATASETS/tom_servo/

cd ~/TextyMcSpeechy/tts_dojo/DATASETS
./create_dataset.sh tom_servo

cd ~/TextyMcSpeechy/tts_dojo/tom_servo_dojo
./run_training.sh

start testing around epoch 5100-5200 and listen. Stop when it sounds good rather than hitting a fixed number.

# manually run export of voice

cd ~/TextyMcSpeechy/tts_dojo/tom_servo_dojo/scripts
bash utils/_tmux_piper_export.sh ../voice_checkpoints/epoch=4684-step=3120040.ckpt ../tts_voices/tom_servo_4684/en_US-tom_servo_4684-medium.onnx tom_servo_dojo

