import os
import subprocess

# Define input and output folders
input_folder = "./"
output_folder = "./processed"
os.makedirs(output_folder, exist_ok=True)

def apply_edge_detection(input_path, output_path):
    """Applies edge detection to a video."""
    command = [
        "ffmpeg", "-i", input_path,
        "-vf", "edgedetect=low=0.1:high=0.4",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(command, check=True)
    print(f"Edge detection applied to {input_path}, saved as {output_path}")

def apply_cropping(input_path, output_path):
    """Automatically detects and crops a video."""
    # Detect crop values
    cropdetect_command = [
        "ffmpeg", "-i", input_path,
        "-vf", "cropdetect=24:16:0",
        "-f", "null", "-"
    ]
    result = subprocess.run(cropdetect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    crop_values = None

    for line in result.stderr.splitlines():
        if "crop=" in line:
            crop_values = line.split("crop=")[1].split()[0]  # Extract crop dimensions

    if crop_values:
        # Apply crop values
        command = [
            "ffmpeg", "-i", input_path,
            "-vf", f"crop={crop_values}",
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Cropped video saved as {output_path}")
    else:
        print(f"Could not detect crop values for {input_path}")

# Iterate through videos in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith((".mp4", ".mkv", ".avi", ".mov")):
        input_path = os.path.join(input_folder, filename)
        
        # User choice: Edge detection or cropping
        print(f"Processing {filename}. Choose an option:")
        print("1. Apply edge detection")
        print("2. Auto-crop video")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            output_path = os.path.join(output_folder, f"edges_{filename}")
            apply_edge_detection(input_path, output_path)
        elif choice == "2":
            output_path = os.path.join(output_folder, f"cropped_{filename}")
            apply_cropping(input_path, output_path)
        else:
            print(f"Invalid choice for {filename}. Skipping...")
