import logging
import sys
import os
import time
import subprocess
import threading
import shutil

# Read folder paths from environment variables or use defaults
input_folder = os.path.abspath(os.environ.get("INPUT_FOLDER", "processmesempai"))
log_dir = os.path.abspath(os.environ.get("LOG_DIR", "bigtrouble"))
output_folder = os.path.abspath(os.environ.get("OUTPUT_FOLDER", "clips"))

# Ensure required directories exist
os.makedirs(input_folder, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Create a log file in the log directory with a timestamped name
log_filename = os.path.join(log_dir, f"log_{time.strftime('%Y%m%d_%H%M%S')}.txt")
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

def consoledivide(x):
    logging.info("\n" + "=" * x + "\n")  # Print a bold divider

# starting the script
consoledivide(50)

# Simple animated loading spinner
spinner_running = False
original_logging_info = logging.info

def stop_spinner():
    global spinner_running
    spinner_running = False

# Monkey-patch logging.info to stop the spinner before logging
def new_logging_info(*args, **kwargs):
    stop_spinner()  # Stop any active spinner
    original_logging_info(*args, **kwargs)

logging.info = new_logging_info

def spinner(message="Loading"):
    spinner_chars = "|/-\\"
    i = 0
    # Write the initial message to the original console output
    original_stdout.write(f"\r{message}... ")
    original_stdout.flush()
    while spinner_running:
        original_stdout.write(spinner_chars[i % len(spinner_chars)])
        original_stdout.flush()
        time.sleep(0.1)
        original_stdout.write("\b")
        i += 1
    # Clear the spinner line once stopped
    original_stdout.write("\r" + " " * (len(message) + 10) + "\r")
    original_stdout.flush()

def animated_loading(message="Loading"):
    global spinner_running
    spinner_running = True
    # Start the spinner in a separate daemon thread
    threading.Thread(target=spinner, args=(message,), daemon=True).start()
    # Return immediately without blocking

logging.info("\nscript codename: orca\n")

# Animated loading with interactivity
animated_loading("The initial loading may take a while...\n\n")

consoledivide(79)

animated_loading("***Importing, one moment please\n")
time.sleep(1)

# leaving here in plain text for now; will fix later
pyannote_auth_token = "PYANNOTE AUTH TOKEN HERE"

import whisperx
import nltk
from clipsai import ClipFinder, Transcriber, MediaEditor, AudioVideoFile, resize
from pyannote.audio import Pipeline

consoledivide(79)
logging.info("packages loaded\n")
time.sleep(2)

logging.info(f"setting up folders...\n")
time.sleep(1)

# Temporary directory for intermediate files
temp_folder = "imthetrashman"
os.makedirs(temp_folder, exist_ok=True)
logging.info(f"'temp' directory named '{temp_folder}'\n")
time.sleep(1)

logging.info(f"Input folder set to '{input_folder}'")
logging.info(f"Clips (output) folder set to '{output_folder}'\n")
time.sleep(2)

logging.info("Setting parameters for whisperX. For more details, visit: https://github.com/m-bain/whisperX")
time.sleep(2)

# Set up custom whisperx model
whisper_arch = "medium"  # Whisper model size: Options include "tiny", "base", "small", "medium", "large"
device = "cpu"         # Device for computation: Options include "cpu", "cuda" (for GPU)
compute_type = "int8"  # Data type for computation: Options include "float16", "float32", "int8"
language = "en"        # {en, fr, de, es, it, ja, zh, nl, uk, pt}

logging.info(f"whisper_arch = '{whisper_arch}'\ndevice = '{device}' \ncompute_type = '{compute_type}'\nlanguage = '{language}'\n")

custom_model = whisperx.load_model(
    whisper_arch=whisper_arch, device=device, compute_type=compute_type, language="en"
)
logging.info("next section loads pyannote auth token\n")
animated_loading("it gives errors often. to begin debug, maybe try checking your huggingface.co token\n")
time.sleep(3)
consoledivide(67)

# Load diarization pipelines
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization@2.1",
    use_auth_token=pyannote_auth_token
)

diarizer = Pipeline.from_pretrained(
    "pyannote/speaker-diarization@2.1",
    use_auth_token=pyannote_auth_token
)

consoledivide(67)

logging.info("setup completed.\n")
animated_loading(f"Counting video files in '{input_folder}'...\n")
time.sleep(2)
# Count all video and (audio=not yet!) files in the input folder
file_count = sum(1 for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mp3', '.wav')))
logging.info(f"\nwe will now begin processing {file_count} videos\n")
time.sleep(1)

logging.info("\nThe time required varies hugely on your computing hardware and selected parameters.\n")
logging.info("Good luck ;/\n")
consoledivide(31)

# this next line is for debugging the diarization pipeline step in the 'try' block'
logging.getLogger('pyannote').setLevel(logging.DEBUG)

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

    # Diarize the extracted audio using the custom PyannoteDiarizer
    import importlib.util

    # Specify the path to your local file, e.g. if it's in the current directory:
    local_diarizer_path = os.path.join("cliaenv", "clipsai", "clipsai", "diarize", "pyannote.py")

    spec = importlib.util.spec_from_file_location("local_pyannote", local_diarizer_path)
    local_pyannote = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(local_pyannote)

    # Now get your custom diarizer class
    PyannoteDiarizer = local_pyannote.PyannoteDiarizer

    try:
        animated_loading("starting diarization... this may take a while")
        
        diarizer = PyannoteDiarizer(auth_token=pyannote_auth_token, device=device)
        
        # Wrap your extracted audio into an AudioFile object. For example:
        from clipsai.media.audio_file import AudioFile  # Make sure this class exists.
        audio_file_obj = AudioFile(extracted_audio_path)
        
        # Call the diarize method, which returns a list of segment dictionaries.
        speaker_segments = diarizer.diarize(
            audio_file=audio_file_obj,
            min_segment_duration=1.5,
            time_precision=6,
        )
        logging.info("Diarization completed. Retrieved speaker segments.")
        
        # Optionally, group segments by speaker if desired:
        speaker_groups = diarizer._group_segments_by_speaker(speaker_segments)
        
        # Now, iterate over the grouped segments. For example:
        for speaker, segments in speaker_groups.items():
            output_dir = os.path.join(output_video_folder, f"Speaker_{speaker}")
            os.makedirs(output_dir, exist_ok=True)
    
    except Exception as e:
        logging.error(f"Error during diarization: {e}")

    # Step 1: Transcribe the video/audio file
    transcriber = Transcriber()
    transcriber._model = custom_model
    transcription = transcriber.transcribe(audio_file_path=extracted_audio_path)

    # Step 2: Find Engaging Clips
    clipfinder = ClipFinder()
    clips = clipfinder.find_clips(transcription=transcription)

    # this is a fast and loose limit of the clip size to 5mins max (we should fix later!!)
    max_clip_duration = 300  # maximum clip duration in seconds (5 minutes)
    filtered_clips = [clip for clip in clips if (clip.end_time - clip.start_time) <= max_clip_duration]
    clips = filtered_clips

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
            # Perform resizing for the clip
            crops = resize(
                video_file_path=input_video_path,
                pyannote_auth_token=pyannote_auth_token,
                aspect_ratio=(9, 16),
                min_segment_duration=clip.end_time - clip.start_time,
                samples_per_segment=11, # 13 is standard. lower numbers are faster at cost of accuracy
            )

            media_editor = MediaEditor()
            media_editor.resize_video(
                original_video_file=media_file,
                resized_video_file_path=clip_output_path,
                width=crops.crop_width,
                height=crops.crop_height,
                segments=[
                    {
                        "start_time": segment.start_time,
                        "end_time": segment.end_time,
                        "x": segment.x,
                        "y": segment.y,
                    }
                    for segment in crops.segments
                    if segment.start_time >= clip.start_time and segment.end_time <= clip.end_time
                ],
            )

            logging.info(f"Resized clip {i + 1} saved to: {clip_output_path}")

        except Exception as e:
            logging.error(f"Error processing clip {i + 1}: {e}")
            continue

    # Instead of moving the processed file to a separate folder, we leave it in place.
    logging.info("Processing complete for this video.")


def ending_sequence(file_count, output_folder):
    logging.info("\nProcessing complete")
    animated_loading("please press 'Enter' to quit")
    logged_input()  # Wait for user confirmation to quit

# Call the ending sequence
ending_sequence(file_count, output_folder)
