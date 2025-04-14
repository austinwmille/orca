import os
import json
import time
import pickle
from PIL import Image, ImageDraw, ImageFont
import subprocess
from datetime import timedelta
import torch
import whisperx
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from openai import OpenAI

# ---------------------------------------------------------------- #
# our folder path
VIDEO_FOLDER_PATH = "./"

load_dotenv('mushroom.env')

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("gptkey")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is not set. Please set it as an environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Path to your OAuth 2.0 Client ID JSON file
CLIENT_SECRET_FILE = './mushroom.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN_PICKLE = 'token.pickle'  # File to store the credentials

def get_authenticated_service():
    creds = None
    # Check if we already have valid credentials saved
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the new credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

# -------------------------------------------------------------------- #

# Transcribe video using Whisper
def transcribe_video(file_path):
    try:
        import whisper
        model = whisper.load_model("medium")  # Use 'small' or 'medium' for better accuracy
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing video: {e}")
        return ""

# Call OpenAI API to generate metadata for a provocative right-wing news clip.
def generate_news_metadata(file_path):
    transcript = transcribe_video(file_path) or "No transcript available."
    original_file_name = os.path.splitext(os.path.basename(file_path))[0]

    prompt = (
        f"Generate YouTube metadata as JSON (title, description, tags, category). It's mostly provacative news segments which we turn in to views and clickbait! RULES:\n"
        f"1. TITLE:\n"
        f"   - Reword the original title (derived from the filename) in a straightforward and mostly-neutral manner. Only include hook words if they clearly add value.\n"
        f"2. DESCRIPTION:\n"
        f"   - Provide a simple, clear description that is not overly dramatic.\n"
        f"   - Do not include generic calls to action except an optional brief note such as (or similar to) 'Subscribe for more digestible clips every week!'.\n"
        f"3. TAGS:\n"
        f"   - Include relevant tags that reflects the content and related material. Don't overuse trendy terms, but we can have some creative license here.\n"
        f"4. CATEGORY:\n"
        f"   - Set the category to 'Entertainment'.\n"
        f"---\n"
        f"IMPORTANT: Return only a valid JSON object with no markdown formatting or additional text.\n"
        f"Filename: {original_file_name}\n"
        f"Transcript: {transcript}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your intended model (e.g., "gpt-4" or "gpt-3.5-turbo")
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant specialized in YouTube metadata optimization for news content."
                },
                {"role": "user", "content": prompt},
            ]
        )
        metadata_content = response.choices[0].message.content.strip()

        # Remove markdown formatting (triple backticks) if present:
        import re
        metadata_content = re.sub(r"^```(?:json)?", "", metadata_content)
        metadata_content = re.sub(r"```$", "", metadata_content)
        metadata_content = metadata_content.strip()

        # Parse the cleaned string into JSON
        metadata = json.loads(metadata_content)

        # Force the category to be 'News'
        metadata['category'] = 'Entertainment'
        metadata['categoryId'] = '27'
        return metadata

    except json.JSONDecodeError:
        print("AI response not in JSON format. Using default metadata.")
        with open('description.txt', 'r', encoding='utf-8') as file:
            description_text = file.read().strip()
        return {
            "title": "Don't like; testing 1",
            "description": description_text,
            "tags": [
                "birds", "parakeets", "budgies", "parakeet", 
                "budgie", "parrot", "parrake", "bird", "fly", "flying", "sky"
            ],
            "categoryId": "27"
        }
    except Exception as e:
        print(f"Error generating metadata: {e}")
        with open('description.txt', 'r', encoding='utf-8') as file:
            description_text = file.read().strip()
        return {
            "title": "Don't like; testing 1",
            "description": description_text,
            "tags": [
                "birds", "parakeets", "budgies", "parakeet", 
                "budgie", "parrot", "parrake", "bird", "fly", "flying", "sky"
            ],
            "categoryId": "27"
        }

def extract_thumbnail(video_file, output_thumbnail):
    """
    Extract a single frame from the middle of the video and save it as the thumbnail.
    """
    # Get the video duration
    cmd_duration = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        video_file
    ]
    try:
        duration_str = subprocess.run(cmd_duration, capture_output=True, text=True, check=True).stdout.strip()
        duration = float(duration_str)
    except Exception as e:
        print(f"Error getting duration for {video_file}: {e}")
        # If error occurs, use a default start time of 10 seconds
        duration = 20.0
    mid = duration / 2

    cmd_extract = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-ss', str(mid),
        '-vframes', '1',
        '-q:v', '2',  # lower value means higher quality
        output_thumbnail
    ]
    try:
        subprocess.run(cmd_extract, check=True)
        print(f"Extracted thumbnail from {video_file} at {mid:.1f} sec")
        return output_thumbnail
    except Exception as e:
        print(f"Error extracting thumbnail from {video_file}: {e}")
        return None


def upload_video(youtube, file_path, metadata):
    # Use metadata description if available; otherwise, fall back to reading description.txt.
    description_text = metadata.get('description')
    if not description_text:
        try:
            with open('description.txt', 'r', encoding='utf-8') as file:
                description_text = file.read().strip()
        except Exception as e:
            print(f"Error reading description.txt: {e}")
            description_text = "No description provided."

    request_body = {
        'snippet': {
            'title': metadata.get('title', "pls don't watch, testing"),
            'description': metadata.get('description', description_text),
            'tags': metadata.get('tags', [
                "birds", "parakeets", "budgies", "parakeet", 
                "budgie", "parrot", "parrake", "bird", "fly", "flying", "sky"
            ]),
            'categoryId': "27",  # Force category to 'News'
        },
        'status': {
            'privacyStatus': 'public',  # Options: 'public', 'unlisted', 'private'
            'selfDeclaredMadeForKids': False  # Default to "Not Made for Kids"
        }
    }

    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {file_path}: {int(status.progress() * 100)}% complete.")
    print(f"Upload completed: {metadata.get('title', 'Untitled Video')}")
    return response
    
# Set the generated thumbnail for a video via the YouTube API.
def set_thumbnail(youtube, video_id, thumbnail_path):
    try:
        response = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print(f"Thumbnail set for video {video_id}")
    except Exception as e:
        print(f"Error setting thumbnail for video {video_id}: {e}")

# Process all video files in the specified folder (only files in the root, not in subfolders).
def process_folder(youtube, folder_path):
    video_files = sorted(
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
    )

    if not video_files:
        print("No video files found in folder:", folder_path)
        return

    part_number = 1
    for file_path in video_files:
        print(f"Processing video: {file_path}")
        metadata = generate_news_metadata(file_path)
        print(f"Generated Metadata: {metadata}")

        # Now, upload the subbed video.
        response = upload_video(youtube, file_path, metadata)
        video_id = response.get("id")
        print(f"Uploaded {file_path} with video ID: {video_id}")

                # Generate and set a custom thumbnail from the video.
        if video_id:
            output_thumbnail = os.path.join(folder_path, f"temp_thumbnail_{part_number}.jpg")
            thumbnail = extract_thumbnail(file_path, output_thumbnail)
            if thumbnail:
                set_thumbnail(youtube, video_id, thumbnail)
            if os.path.exists(output_thumbnail):
                os.remove(output_thumbnail)
        else:
            print("Skipping thumbnail generation due to missing video ID.")

        print("Waiting 5 minutes before processing next clip.")
        time.sleep(300)  # Wait 10 minutes (600 seconds)

        # Delete the file after upload.
        if os.path.exists(file_path):
            os.remove(file_path)

        part_number += 1

# Main function
def main():
    youtube = get_authenticated_service()
    if os.path.exists(VIDEO_FOLDER_PATH) and os.path.isdir(VIDEO_FOLDER_PATH):
        process_folder(youtube, VIDEO_FOLDER_PATH)
    else:
        print(f"Folder not found: {VIDEO_FOLDER_PATH}")

if __name__ == '__main__':
    main()
