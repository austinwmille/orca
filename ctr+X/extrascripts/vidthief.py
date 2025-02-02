import yt_dlp

LOG_FILE = 'downloaded_urls.txt'

def load_downloaded_urls():
    """Load already downloaded URLs from the log file."""
    try:
        with open(LOG_FILE, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_downloaded_url(url):
    """Save a newly downloaded URL to the log file."""
    with open(LOG_FILE, 'a') as file:
        file.write(url + '\n')

def download_video(url):
    """Download video from a given URL."""
    # Download options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Prioritize separate streams, fallback to single best
        'merge_output_format': 'mp4',  # Ensure output is always MP4
        'outtmpl': '%(uploader)s/%(upload_date)s-%(title)s.%(ext)s',  # Metadata-rich filenames
        'sanitize_filename': True,  # Remove special characters from filenames
        'quiet': False,  # Show progress
    }

    # Attempt download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Skipping video due to error: {e}")

def main():
    # Load downloaded URLs
    downloaded_urls = load_downloaded_urls()

    # List of video URLs (replace or extend as needed)
    # don't forget to put a comma after them!!
    video_urls = [
        "https://www.youtube.com/watch?v=ZN5PoW7_kdA",  # Example YouTube URL
        "https://www.youtube.com/watch?v=2yJgwwDcgV8",  # Example Vimeo URL
        "https://www.youtube.com/shorts/2RnO2WnSTQ0",  # Example Dailymotion URL
        "https://www.youtube.com/shorts/n3x8clbCY9A",
        "https://www.youtube.com/watch?v=Cqd1Gvq-RBY",
        "https://www.youtube.com/watch?v=mLyOj_QD4a4",
        "https://www.youtube.com/watch?v=k1BneeJTDcU",
        "https://www.youtube.com/shorts/aFisWf9PNu8",
        "https://www.youtube.com/shorts/aFisWf9PNu8",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        # Add more video URLs here
    ]

    for url in video_urls:
        if url not in downloaded_urls:
            print(f"Downloading: {url}")
            download_video(url)  # Download the video
            save_downloaded_url(url)  # Log the URL
            print(f"Downloaded and logged: {url}")
        else:
            print(f"Already downloaded: {url}")

if __name__ == "__main__":
    main()
