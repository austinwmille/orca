import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from transformers import pipeline  # For AI-generated text

# Paths and API setup
CLIENT_SECRET_FILE = 'path/to/your/secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
videos_folder = "./memes"  # Folder containing videos to upload
uploaded_folder = './uploaded'  # Folder for uploaded videos
os.makedirs(uploaded_folder, exist_ok=True)

# Function to authenticate YouTube API
def get_authenticated_service():
    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    return build('youtube', 'v3', credentials=credentials)

# Function to auto-generate metadata
def generate_metadata(video_file):
    # Analyze the video file (simplified, e.g., extract filename keywords)
    base_name = os.path.splitext(video_file)[0]
    # Generate AI-based title and description
    summarizer = pipeline("summarization")
    summary = summarizer(f"This is a video about {base_name}", max_length=20, min_length=5, do_sample=False)
    title = f"{base_name.capitalize()} - Viral Video!"
    description = f"Check out this amazing video: {summary[0]['summary_text']}\n#viral #trending"
    tags = [base_name, "trending", "viral", "video"]
    return title, description, tags

# Function to upload video
def upload_video(youtube, file_path, title, description, tags):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '24',  # Category ID for Entertainment
        },
        'status': {
            'privacyStatus': 'public'
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
            print(f"Uploading {file_path}: {int(status.progress() * 100)}%")
    print(f"Upload completed: {title}")
    return response

# Main function
def main():
    youtube = get_authenticated_service()
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov'))]
    
    for video_file in video_files:
        file_path = os.path.join(videos_folder, video_file)
        title, description, tags = generate_metadata(video_file)
        
        print(f"Uploading: {file_path}")
        upload_video(youtube, file_path, title, description, tags)
        
        # Move uploaded video to the uploaded folder
        shutil.move(file_path, os.path.join(uploaded_folder, video_file))
        time.sleep(10)  # Avoid hitting API limits

if __name__ == '__main__':
    main()
