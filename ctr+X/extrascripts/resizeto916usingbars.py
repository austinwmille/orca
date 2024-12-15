import os
import subprocess

def resize_video_to_tiktok(input_path, output_path):
    """
    Resize a video to 9:16 aspect ratio for TikTok using FFmpeg.
    :param input_path: Path to the input video file.
    :param output_path: Path to save the resized output video.
    """
    if not os.path.exists(input_path):
        print("Input file does not exist.")
        return
    
    # Corrected FFmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale='if(gte(iw/ih,9/16),1080,-1)':'if(gte(iw/ih,9/16),-1,1920)',pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",
        output_path
    ]
    
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video resized and saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error resizing video:", e)

# Example usage
input_video = "C:\\Users\\austi\\Desktop\\WIPs\\tiktok backlog\\nipstok\\nipstok1.mp4"
output_video = "vines_that_julienne_my_carrots.mp4"
resize_video_to_tiktok(input_video, output_video)
