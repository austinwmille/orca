import logging
import sys
import os
import time
import subprocess

log_filename = f"bigtrouble/log_{time.strftime('%Y%m%d_%H%M%S')}.txt"  # Unique filename with timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Log to file
        logging.StreamHandler(sys.stdout),  # Also log to console
    ],
)

# Preserve original stdout for console output
original_stdout = sys.stdout

# Redirect stdout and stderr to the log file
sys.stdout = open(log_filename, "a")
sys.stderr = open(log_filename, "a")

logging.getLogger().setLevel(logging.INFO)

def logged_input(prompt=""):
    original_stdout.write(prompt)  # Display prompt in the console
    original_stdout.flush()
    user_input = input()  # Use normal input to capture user response
    logging.info(f"User input: {user_input}")  # Log the input
    return user_input

def softclear():
    logging.info("\n" * 10)  # Print 100 blank lines to push previous output out of view

def consoledivide(x):
    logging.info("\n" + "=" * x + "\n")  # Print a bold divider

# starting the script
#softclear() is optional here to give a clear screen
consoledivide(50)

# Simple animated loading spinner
def animated_loading(message="Loading"):
    """Displays an animated spinner in the console only."""
    spinner = "|/-\\"
    original_stdout.write(f"\r{message}... ")
    for _ in range(10):  # Control the length of the animation
        for frame in spinner:
            original_stdout.write(frame)
            original_stdout.flush()
            time.sleep(0.1)
            original_stdout.write("\b")  # Erase the spinner character

# Starting page with print statements and delay
logging.info("\nWelcome to nips' ctr+X script!\n")
time.sleep(2)
logging.info("\nWe are currently using clipmeV2\n")

# Animated loading with interactivity
animated_loading("\nPlease press 'Enter' when you're ready to continue.\n")
logged_input()  # Wait for user input

animated_loading("Importing, one moment please\n")
time.sleep(1)

# Animated loading with interactivity
animated_loading("You're about to see a bunch of text..\nAlso, it may take a few minutes\n\n")

consoledivide(79)

#leaving here in plain text for now; will fix later
pyannote_auth_token = "your pyannote access token goes here"

import shutil
import whisperx
import nltk
from clipsai import ClipFinder, Transcriber, MediaEditor, AudioVideoFile, resize
from pyannote.audio import Pipeline

consoledivide(79)
logging.info("\nWe're past the first hurdle! Wasn't that fun??\n")
time.sleep(2)

logging.info(f"Ensuring existence of Danny Devito..\n")
time.sleep(1)
# Temporary directory for intermediate files (ensure it exists)
temp_folder = "imthetrashman"
os.makedirs(temp_folder, exist_ok=True)
logging.info(f"'temp' directory named '{temp_folder}'\n")
time.sleep(1)

logging.info(f"setting up our folders...\n")
time.sleep(1)
# Input and output directories (use absolute paths)
input_folder = os.path.abspath("processmesempai")  
processed_folder = os.path.abspath("done")
output_folder = os.path.abspath("ctrs")

os.makedirs(input_folder, exist_ok=True)
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Define path for extracted audio (this may be overridden per file)
# right now we are using temp_folder but we can change later
extracted_audio_path = os.path.join(temp_folder, "extracted_audio.wav")

logging.info(f"folder to put your long videos in: '{input_folder}'\n")
logging.info(f"clips created will be stored in '{output_folder}'\n")
logging.info(f"after processing, og video files will move from '{input_folder}' to '{processed_folder}'\n\n")
time.sleep(2)

animated_loading("Please read those paths.. you don't have to remember them\n")

logging.info(f"loading some conditions for the AI model (you can play around with the values in the script)\n")
time.sleep(2)

# Set up custom whisperx model
whisper_arch = "base"  # Whisper model size: Options include "tiny", "base", "small", "medium", "large"
device = "cpu"         # Device for computation: Options include "cpu", "cuda" (for GPU)
compute_type = "int8"  # Data type for computation: Options include "float16", "float32", "int8"
language = "en"        # {en, fr, de, es, it, ja, zh, nl, uk, pt}
#batch_size = "4, 8, 16, others?"  this parameter gave me trouble but i think it's available

logging.info(f"whisper_arch = '{whisper_arch}'\ndevice = '{device}' \ncompute_type = '{compute_type}'\nlanguage = '{language}'\n")

custom_model = whisperx.load_model(
    whisper_arch=whisper_arch, device=device, compute_type=compute_type, language="en"
)
logging.info("\nuhhh, just ignore that btw. mine always says that ;)\n\n")
logging.info("ALRIGHT! we are going to load our pyannote token now\n")
animated_loading("it gives errors often, so please read and debug the following log if it kicks you out\n\ntry renewing your huggingface.co token\nOR you can try just copy/paste into chatgpt")
time.sleep(3)
logged_input("press enter when ready")
consoledivide(67)

# Load diarization pipelines
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=pyannote_auth_token
)
diarizer = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=pyannote_auth_token
)

consoledivide(67)

logging.info("success!! you've done great so far\n\n")
animated_loading(f"Counting video files in '{input_folder}'...\n")
time.sleep(1)
# Count all video and (audio=not yet!) files in the input folder
file_count = sum(1 for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mp3', '.wav')))
logging.info(f"Total videos found: {file_count}")
time.sleep(1)

consoledivide(31)
logging.info("sweet! the next part will take FOREVER, be warned!\n")
time.sleep(1)
logging.info("if this is your first time using this script,\nthen you should probably make sure\nonly ONE video is in the "+input_folder+" folder")
time.sleep(2)
input("okay, then, press 'enter' if you wanna go for it...")
animated_loading()
consoledivide(31)

# Process each video/audio file in the input folder
for video_file in os.listdir(input_folder):
    if not video_file.lower().endswith(('.mp4', '.mov', '.avi', '.mp3', '.wav')):
        continue

    # Define paths for each video/audio file
    input_video_path = os.path.join(input_folder, video_file)
    video_base_name = os.path.splitext(os.path.basename(input_video_path))[0]
    extracted_audio_path = os.path.join(temp_folder, f"{video_base_name}_audio.wav")
    output_video_folder = os.path.join(output_folder, video_base_name)
    os.makedirs(output_video_folder, exist_ok=True)

    logging.info(f"Processing video/audio file: {input_video_path}")

    # Step 0: Extract Audio (Explicitly)
    media_file = AudioVideoFile(input_video_path)
    wav_file = media_file.extract_audio(
        extracted_audio_file_path=extracted_audio_path,
        audio_codec="pcm_s16le",
        overwrite=True
    )
    logging.info(f"Audio extracted to: {extracted_audio_path}")

    # Diarize the extracted audio
    # Adjust this logic based on pyannote's actual return structure.
    try:
        speaker_groups = diarizer.diarize(extracted_audio_path)
        for speaker, segments in speaker_groups.items():
            output_dir = os.path.join(output_video_folder, f"Speaker_{speaker}")
            os.makedirs(output_dir, exist_ok=True)
            for segment in segments:
                save_clip(extracted_audio_path, segment, output_dir)
    except Exception as e:
        logging.error(f"Error during diarization: {e}")

    # Step 1: Transcribe the video/audio file
    transcriber = Transcriber()
    transcriber._model = custom_model
    transcription = transcriber.transcribe(audio_file_path=extracted_audio_path)

    # Step 2: Find Engaging Clips
    clipfinder = ClipFinder()
    clips = clipfinder.find_clips(transcription=transcription)

    # Output the results of the clipfinder
    for i, clip in enumerate(clips):
        logging.info(f"Clip {i + 1}: Start={clip.start_time}, End={clip.end_time}")

    # Step 3: Resize each clip based on speaker focus
    seen_clips = set()

    for i, clip in enumerate(clips):
        clip_key = (clip.start_time, clip.end_time)
        #if clip_key in seen_clips:
        #    logging.info(f"Skipping duplicate clip: {clip_key}")
        #    continue
        #seen_clips.add(clip_key)

        clip_filename = f"{video_base_name}_clip{i + 1}.mp4"
        clip_output_path = os.path.join(output_video_folder, clip_filename)

        logging.info(f"Processing clip {i + 1}: {clip_key} -> {clip_output_path}")

        try:
            # Commenting out resizing for now to resolve issues
            # Perform resizing for the clip
            #crops = resize(
            #    video_file_path=input_video_path,
            #    pyannote_auth_token=pyannote_auth_token,
            #    aspect_ratio=(9, 16),
            #    min_segment_duration=clip.end_time - clip.start_time,
            #    samples_per_segment=9,
            #)

            #media_editor = MediaEditor()
            #media_editor.resize_video(
            #    original_video_file=media_file,
            #    resized_video_file_path=clip_output_path,
            #    width=crops.crop_width,
            #    height=crops.crop_height,
            #    segments=[
            #        {
            #            "start_time": clip.start_time,
            #            "end_time": clip.end_time,
            #            "x": segment.x,
            #            "y": segment.y,
            #        }
            #        for segment in crops.segments
            #    ],
            #)

            logging.info(f"Resized clip {i + 1} saved to: {clip_output_path}")

        except Exception as e:
            logging.error(f"Error processing clip {i + 1}: {e}")
            continue

    # Move processed video/audio to the processed folder
    processed_path = os.path.join(processed_folder, video_file)
    shutil.move(input_video_path, processed_path)
    logging.info(f"Moved processed file to: {processed_path}")


def ending_sequence(file_count, output_folder, processed_folder):
    logging.info("\nScript Completed!")
    logging.info(f"Total files processed: {file_count}")
    logging.info(f"Processed files saved in: {output_folder}")
    logging.info(f"Original files moved to: {processed_folder}")
    animated_loading("Okay then, press 'Enter' to quit, I guess?")
    input()  # Wait for user confirmation to quit

# Call the ending sequence
ending_sequence(file_count, output_folder, processed_folder)
