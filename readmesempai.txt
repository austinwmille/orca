--------------------------------------------
nips' orca script (previously ctr+x)

This application takes a video and extracts the audio. Using whisperX (https://github.com/m-bain/whisperX and https://arxiv.org/abs/2303.00747) it transcribes the audio. It then uses clipsai to analyze the transcript in an attempt to determine shifts in topic and segments which could function as stand-alone, coherent clips (https://www.clipsai.com/references/clip and this arxiv paper https://arxiv.org/abs/2106.12978). After this it performs diarization using pyannote (https://github.com/pyannote/pyannote-audio) to determine speakers in the audio file. This data is stored in a dictionary containing speaker_number and timestamps. It will (i'm not an expert on this; please see the arxiv papers) use the audio, its transcription, arbitrary frames, changes in content and subject matter, voice inflections/pauses, et cetera, to trim the video into clips AND resize the clips to a given aspect ratio while keeping the speaker in the frame.

This is pretty awesome that it works at all. And after playing with it a lot it works pretty fucking well actually, so don't give up. 

The intended use case for this includes podcasts, longer interviews, panel discussions, and similar stuff. 

I am certain that some of the particulars above are incorrect, but it gives a pretty solid understanding to start with. 

Almost the entirety of the work can be found at (clipsai.com). clipsai is an open source python package literally made to do this. I had a ton of trouble getting it to work as-is online, which is why I am putting this here at all, and i don't think there has been an update in over a year.

This project is mostly for myself, and maybe a few interested friends. Feel free to use it and please reach out to me if you do! 

Last note: almost all of it is broken so be ready to debug (i am literally so sorry)


What follows are the first instructions I wrote for the script. All of it is no-op now and containerized-- except step 2! Step 2 contains the individual huggingface links to various gated ML/LLM models which you will need to request access to.

-------------------------------------------
Okay, then, here's how to get started -- good luck:
  ( please note, it's VERY picky and a wip )
  ( still mostly optimized for my computer, sorry! )

0. Before anything, open a console and install ffmpeg and libmagic. idk if you have to do this since I am trying to include them in the environment one day, but if you are a person who would read this far then you should have them installed anyway apart from this project.

1. Install python3.8 on your machine. Really any version of python should work and idk why this isn't the case. Anyway, if you're on windows and have never used python (that's weird) you can download it online.
(likely you'll have to download it online and install it)

2. Go to (huggingface.co). This is a website which allows free access to open source large language models. You will have to create an account, but you can just log in with google. Many of the models we are going to use are 'gated'. I am guessing this just means that they kinda want a real person to use them and not just used 24/7 at max by automated things. Anyway, you'll have to 'request access' by just pushing a button once you have a HF account. Here are some of them that i've had to access in the process of getting the script to work:
  a.  https://huggingface.co/pyannote/segmentation
  b.  https://huggingface.co/pyannote/speaker-diarization-3.1
  c.  https://huggingface.co/pyannote/speaker-diarization
  d.  https://huggingface.co/pyannote/speaker-segmentation
  e.  https://huggingface.co/pyannote/speaker-diarization-3.0
  f.  https://huggingface.co/pyannote/segmentation-3.0

 2.1  Still on huggingface, go to the top right and click on your profile photo to see your account options. GO TO ACCESS TOKENS. Create a new token and fucking save that shit to a text file on your desktop or something.

3. open clipmev2.py in a code/text editor. Your pyannote ACCESS TOKEN should go into line 44 between the quotes. save please.
  xa.  lines 52-83 define the names of the folders, you can edit them but maybe try that after it's working
  xb.  lines 89-93 set some parameters for the audio parsing package whisperx. i think this does a HUGE amount of the ai work (if not all of it). (https://github.com/m-bain/whisperX) I believe this is (or was) an OpenAI project so that should give some idea of how compute intensive this script is. anyway, you can experiment with these values if you want.
===========================
4.  okay, let's run it!

open a console and navigate to the main directory 'ctr+X'

activate env, type: ./cliaenv/scripts/activate
   (did you see a change??)

LETSGO, type: python ./clipmev2.py
  (maybe python38, py, it might be different! to test before running type: python --version, or py --version, or python38 --version, etc to see what command gives version 3.8. then use that one in this line)

5.  best of fucking luck, friend. hit me up if you want
