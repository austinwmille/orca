# if a folder contains many subfolders with files in them,
#this script will go thru a subfolder
#and move the files (with certain extension. see line 19) 
#from the subfolder to the root folder (cd ..)
# it does this for every subfolder in the root folder

import os
import shutil

# Set the path of the main folder where all subfolders with videos are located
main_folder_path = "./"

# Loop through all files in the subdirectories of the main folder
for root, dirs, files in os.walk(main_folder_path):
    for file in files:
        # Construct full file path
        file_path = os.path.join(root, file)
        
        # Only move video files (you can adjust extensions as needed)
        if file.endswith((".mp4", ".mkv", ".avi", ".mov")):
            try:
                # Move the file to the main folder
                shutil.move(file_path, main_folder_path)
                print(f"Moved: {file}")
            except Exception as e:
                print(f"Could not move {file}: {e}")

# Remove empty subfolders
for root, dirs, files in os.walk(main_folder_path, topdown=False):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):  # Check if the directory is empty
            os.rmdir(dir_path)
            print(f"Removed empty folder: {dir_path}")
