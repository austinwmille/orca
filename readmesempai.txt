current line used to run docker container. please edit with your own paths

docker run --rm -it --env-file "${PWD}\.env" -v "${PWD}\processmesempai:/app/processmesempai" -v "${PWD}\bigtrouble:/app/bigtrouble" -v "${PWD}\clips:/app/clips" -v "${HOME}\.cache\huggingface:/root/.cache/huggingface" -v "${HOME}\.cache\torch:/root/.cache/torch" -e INPUT_FOLDER=/app/processmesempai -e LOG_DIR=/app/bigtrouble -e OUTPUT_FOLDER=/app/clips orca:beta

--------------------------------------------
nips' orca script (previously ctr+x)

This application takes a video and extracts the audio. Using whisperX (https://github.com/m-bain/whisperX and https://arxiv.org/abs/2303.00747) it transcribes the audio. It then uses clipsai to analyze the transcript in an attempt to determine shifts in topic and segments which could function as stand-alone, coherent clips (https://www.clipsai.com/references/clip and this arxiv paper https://arxiv.org/abs/2106.12978). After this it performs diarization using pyannote (https://github.com/pyannote/pyannote-audio) to determine speakers in the audio file. This data is stored in a dictionary containing speaker_number and timestamps. It will (i'm not an expert on this; please see the arxiv papers or literally anyone else who knows what llm diarization means) use the audio, its transcription, arbitrary frames, changes in content and subject matter, voice inflections/pauses, et cetera, to trim the video into clips AND resize the clips to a given aspect ratio while keeping the speaker in the frame.

This is pretty awesome that it works at all. And after playing with it a lot it works pretty fucking well actually, so don't give up. 

The intended use case for this includes podcasts, longer interviews, panel discussions, and similar stuff. 

I am certain that some of the particulars above are incorrect, but it gives a pretty solid understanding to start with. 

Almost the entirety of the work can be found at (clipsai.com). clipsai is an open source python package literally made to do this. I had a ton of trouble getting it to work as-is online, which is why I am putting this here at all, and i don't think there has been an update in over a year.


What follows are the first instructions I wrote for the script. It is now containerizable, so the instructions are useless. Except step 2, though, which contains the individual huggingface links to various gated ML/LLM models which you will need to request access to. **I think now only one or two of them are actually required, but it took me a while to figure that out.

-------------------------------------------

2. Go to (huggingface.co). This is a website which allows free access to open source large language models. You will have to create an account, but you can just log in with google. Many of the models we are going to use are 'gated'. I am guessing this just means that they kinda want a real person to use them and not just used 24/7 at max by automated things. Anyway, you'll have to 'request access' by just pushing a button once you have a HF account. Here are some of them that i've had to access in the process of getting the script to work:
  a.  https://huggingface.co/pyannote/segmentation
  b.  https://huggingface.co/pyannote/speaker-diarization-3.1
  c.  https://huggingface.co/pyannote/speaker-diarization
  d.  https://huggingface.co/pyannote/speaker-segmentation
  e.  https://huggingface.co/pyannote/speaker-diarization-3.0
  f.  https://huggingface.co/pyannote/segmentation-3.0

 2.1  Still on huggingface, go to the top right and click on your profile photo to see your account options. GO TO ACCESS TOKENS. This token will go in the .env file.