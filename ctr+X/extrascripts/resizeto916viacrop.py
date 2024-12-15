import os
import subprocess
import json
import random
from datetime import datetime

def generate_random_name():
    # Define a list of chaotic nonsense names
    random_names = [
    "GlitterDragon",
    "SpicyPenguin",
    "ChaosMuffin",
    "ExplodingRainbow",
    "PixelatedLlama",
    "QuantumDonkey",
    "TurboSocks",
    "ElectricToast",
    "BananaOverdrive",
    "WaffleHurricane",
    "AngryTurnip77",
    "RainbowBacon95",
    "ToasterFury",
    "FlamingNachos",
    "NinjaPotato",
    "LaserUnicorn",
    "SparklePanda",
    "CosmicTaco",
    "GalaxyShrimp",
    "NeonSloth",
    "AstroPickle",
    "TurboPenguin",
    "ElectricBurrito",
    "CaptainCactus",
    "BionicFlamingo",
    "HyperWaffles",
    "MegaPineapple",
    "CyberOtter",
    "AtomicMango",
    "IntergalacticZebra",
    "PsychicSalad",
    "StealthHamster",
    "RocketKoala",
    "InfinityToast",
    "FunkyWalrus",
    "ZebraFusion",
    "TacoVortex",
    "TurboBanana",
    "MysticMeatball",
    "SonicNoodles",
    "BobaThunder",
    "FrostyOctopus",
    "PunkPinecone",
    "DancingAvocado",
    "CucumberCannon",
    "FeralCupcake",
    "YetiTaco",
    "ThunderWaffles",
    "MoonLobster",
    "SpeedyCabbage",
    "DiscoSausage",
    "WarpDriveDonut",
    "CosmicPinecone",
    "QuantumLobster",
    "AstroMuffin",
    "FunkyChicken",
    "DoomPickle",
    "ShadowPotato",
    "RocketParrot",
    "TurboTangerine",
    "NeonCabbage",
    "LaserBeetle",
    "PsychoBanana",
    "BerserkSquirrel",
    "MysticMoose",
    "TacoTyphoon",
    "CaptainPineapple",
    "ElectricMongoose",
    "StealthMango",
    "CactusExplosion",
    "SassyCarrot",
    "HyperCucumber",
    "WittyZebra",
    "ChocoThunder",
    "CosmicCarrot",
    "SpicySloth",
    "QuantumMeatloaf",
    "TurboPlatypus",
    "NoodleStorm",
    "DiscoShrimp",
    "AtomicWalnut",
    "FunkyPlatypus",
    "JellyBeanChaos",
    "SonicBaguette",
    "MoonPickle",
    "GalaxyWombat",
    "NuclearWaffles",
    "ShadowLettuce",
    "CaptainBiscuit",
    "VortexSquid",
    "WarpDriveLlama",
    "RogueDoughnut",
    "CyberCarrot",
    "AstroWombat",
    "PsychedelicLobster",
    "CosmicCroissant",
    "StealthOnion",
    "TurboSalmon",
    "RainbowBison",
    "DoomBagel",
    "ElectricGiraffe",
    "CaptainSprinkles",
    "RocketChurro",
    "SassyToast",
    "FeralLasagna",
    "BionicWaffles"
]
    
    # Select a random name from the list
    random_name = random.choice(random_names)

    # Get today's date in YYYY-MM-DD format
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Add a random number between 13 and 97 to the end of the name
    random_number = random.randint(13, 97)
    random_name_with_number = f"{random_name}{random_number}"

    # Combine the random name, today's date, and the tag
    new_filename = f"{random_name_with_number}_{today_date}_{'{nips42069}'}"
    return new_filename

def get_video_dimensions(video_path):
    """
    Use ffprobe to get video dimensions (width and height).
    Returns (width, height) as integers.
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"ffprobe failed: {result.stderr}")

    info = json.loads(result.stdout)
    width = info["streams"][0]["width"]
    height = info["streams"][0]["height"]
    return width, height

def calculate_fontsize(w, ih, text, base_fontsize, scaling_factor=0.5, min_height_ratio=0.05, max_width_ratio=0.85):
    # Estimate max font size based on width
    max_fontsize_width = w * max_width_ratio / (len(text) * scaling_factor)

    # Ensure font size is at least a percentage of the video height
    min_fontsize = int(ih * min_height_ratio)

    # Take the smaller of the two limits to ensure text fits comfortably
    return max(min(base_fontsize, int(max_fontsize_width)), min_fontsize)

def calculate_fontsize2(w, ih, text, base_fontsize, scaling_factor=0.8, min_height_ratio=0.04, max_width_ratio=0.65):
    # Estimate max font size based on width
    max_fontsize_width = w * max_width_ratio / (len(text) * scaling_factor)

    # Ensure font size is at least a percentage of the video height
    min_fontsize = int(ih * min_height_ratio)

    # Take the smaller of the two limits to ensure text fits comfortably
    return max(min(base_fontsize, int(max_fontsize_width)), min_fontsize)

def crop_video_to_9_16(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Input file {input_path} does not exist.")
        return

    try:
        iw, ih = get_video_dimensions(input_path)
    except Exception as e:
        print(f"Error getting video dimensions for {input_path}: {e}")
        return

    # Calculate dimensions for 9:16 aspect ratio with no horizontal cropping
    target_width = iw
    target_height = round(iw * 16 / 9)  # Calculate height based on 9:16 aspect ratio

    # Add black bars to pad vertically if needed
    pad_filter = f"pad=width={iw}:height={target_height}:x=0:y=(oh-ih)/2:color=black"

    # dynamically change the font size:
    aspect_ratio = iw / ih
    font_scaling_factor = 1 if aspect_ratio >= 9/16 else aspect_ratio / (9/16)
    min_font_size = 28  # Define a minimum font size for readability
    # Replace fontdynamo calculations
    fontdynamo1 = calculate_fontsize(iw, ih, "If only there was a page dedicated to", base_fontsize=27)
    fontdynamo2 = calculate_fontsize2(iw, ih, "\"If only there was a page dedicated to...\"", base_fontsize=20)
    fontdynamo3 = calculate_fontsize(iw, ih, "~ GOLDEN VIRAL EDITION XD ~", base_fontsize=30)

    # dynamically calulate position of drawtexts based on video height
    # this helps for going thru a folder with many different aspect ratios
    dynamoy1 = 0.07 * target_height  # Example: 5% from the top
    dynamoy2 = 0.11*target_height
    dynamoy3 = 0.15*target_height
    dynamoy4 = 0.19*target_height  # this one is for watermark_drawtext but unused rn

    # Drawtext for overlaying text in the black bars
    font_path = "C\\:/Windows/Fonts/verdana.ttf"
    font_path_golden = "C\\:/Windows/Fonts/TEMPSITC.TTF"

    drawtext_filter = (
        f"drawtext=fontfile='{font_path}':"
        f"text='If only there was a page dedicated to':"
        f"x=(w-text_w)/2:y={int(dynamoy1)}:"  # Adjusted y position to fit in the top bar
        f"fontcolor=#AAA6FF:fontsize={fontdynamo1}:line_spacing=3:borderw=2:bordercolor=black:box=1:boxcolor=black@0.7,"
        
        f"drawtext=fontfile='C\\:/Windows/Fonts/comicz.ttf':"
        f"text='\"If only there was a page dedicated to...\"':"
        f"x=(w-text_w)/2:y={int(dynamoy2)}:"  # Adjusted y position for next line
        f"fontcolor=#AAA6FF:fontsize={fontdynamo2}:line_spacing=5:borderw=1:bordercolor=purple:box=1:boxcolor=black@0.7,"
        
        f"drawtext=fontfile='{font_path}':"
        f"text='videos':"
        f"x=(w-text_w)/2:y={int(dynamoy3)}:"  # Adjusted y position for "videos"
        f"fontcolor=#AAA6FF:fontsize={fontdynamo1}:line_spacing=3:borderw=2:bordercolor=black:box=1:boxcolor=black@0.7,"
        
        f"drawtext=fontfile='{font_path_golden}':"
        f"text='~ GOLDEN VIRAL EDITION XD ~':"
        f"x=(w-text_w)/2:y={int(dynamoy4)}:"  # Adjusted y position for the golden text
        f"fontcolor=#FFD700:fontsize={fontdynamo3}:line_spacing=6:borderw=2:shadowcolor=goldenrod:shadowx=1:shadowy=1:bordercolor=black:box=1:boxcolor=black@0.7"
    )

    # Drawtext for watermark
    watermark_drawtext = (
        f"drawtext=fontfile='C\\:/Users/austi/AppData/Local/Microsoft/Windows/Fonts/Caveat-Medium.ttf':"
        f"text='nips42069':"
        f"x=(w-text_w-30):y=({ih}-text_h-0):"  # Bottom-right corner with padding
                                              # The above is a lie. it is on top of the video now and aligned with ih instead of with h
        f"fontcolor=red@0.5:fontsize={fontdynamo2}:borderw=1:bordercolor=black:shadowcolor=black:box=1:boxcolor=black@0.07"
    )

    # Combine filters
    vf_filter = f"{pad_filter},{drawtext_filter},{watermark_drawtext}"

    # FFmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-filter_complex", vf_filter,
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
        print(f"Video processed and saved to: {os.path.abspath(output_path)}")
    except subprocess.CalledProcessError as e:
        print("Error processing video:", e)

def batch_crop_videos(input_folder, output_folder):
    """
    Crop all mp4 videos in input_folder and save them in output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all .mp4 files in the input_folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            
            # Generate a new random filename
            new_filename = generate_random_name()
            output_path = os.path.join(output_folder, f"{new_filename}.mp4")

            print(f"Processing {filename} as {new_filename}.mp4...")
            crop_video_to_9_16(input_path, output_path)

input_dir = r"C:\Users\austi\Desktop\WIPs\tiktok backlog\nipstok\go thru these\individual meme vids"
output_dir = r"C:\Users\austi\Desktop\WIPs\tiktok backlog\nipstok\check before upload"

batch_crop_videos(input_dir, output_dir)
