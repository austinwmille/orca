----------------------------------------------------------------
nips' orca script (previously ctr+x)

This application takes a video and extracts the audio. Using whisperX (https://github.com/m-bain/whisperX and https://arxiv.org/abs/2303.00747) it transcribes the audio. It then uses clipsai to analyze the transcript in an attempt to determine shifts in topic and segments which could function as stand-alone, coherent clips (https://www.clipsai.com/references/clip and this arxiv paper https://arxiv.org/abs/2106.12978). After this it performs diarization using pyannote (https://github.com/pyannote/pyannote-audio) to determine speakers in the audio file. This data is stored in a dictionary containing speaker_number and timestamps. 

I am not sure what happens next, honestly, and I really don't care. Please see the arxiv papers or literally anyone else for greater insight. After the above paragraph it does something like this: It will use the audio, its transcription, arbitrary frames, changes in content and subject matter, voice inflections/pauses, et cetera, to trim the video into clips AND resize the clips to a given aspect ratio while keeping the speaker in the frame.

This is pretty awesome that it works at all. And after playing with it a lot it works pretty well actually, so don't give up. 

The intended use case for this includes podcasts, longer interviews, panel discussions, and similar stuff. Other similar stuff will work too, but if a clip has many speakers or faces (i.e. a wide shot of a speech from Congress) then it becomes much more difficult to determine which face the audio is 'coming from'. Also it will use a ridilously large amount of memory.

I am certain that some of the particulars above are incorrect, but it gives a decent understanding to start and will give some insight when it breaks. 

Almost the entirety of the work can be found at (clipsai.com). clipsai is an open source python package literally made to do this. I had a ton of trouble getting it to work as-posted, which is why I am putting this here at all, and I don't think there has been an update in over a year. If you follow the (only 4 or 5) lines in the quickstart section of that repo you run into dependency conflicts immediately. whisperx has had much more development than the clipsai package which I believe is related to the problem.

I have gotten it to work with loads of help from LLMs (mostly chatGPT honestly) . I have attempted to pin some requirements. I have dockerized it. I found that patching one of the whisperX scripts after installation has helped. The project is super patch-worked and the script is dumb and filled with bloat. But it works. 

----------------------------------------------------------------

MY current line used to run docker container in case it helps. please edit with your own paths

docker run --rm -it --env-file .env -v "${PWD}\processmesempai:/app/processmesempai" -v "${PWD}\bigtrouble:/app/bigtrouble" -v "${PWD}\clips:/app/clips" -v "${HOME}\.cache\huggingface:/root/.cache/huggingface" -v "${HOME}\.cache\torch:/root/.cache/torch" -e INPUT_FOLDER=/app/processmesempai -e LOG_DIR=/app/bigtrouble -e OUTPUT_FOLDER=/app/clips orca:gamma

----------------------------------------------------------------
Here are some instructions:

They contain the individual huggingface links to various gated ML/LLM models which you will need to request access to. **I think now only one or two of them are actually required, but it took me a while to figure that out.**

1. Create a Hugging Face account & request model access
   Required:
     https://huggingface.co/pyannote/segmentation
     https://huggingface.co/pyannote/speaker-diarization-3.1
   Optional (if you hit missing-model errors):
     https://huggingface.co/pyannote/speaker-diarization
     https://huggingface.co/pyannote/speaker-segmentation
     https://huggingface.co/pyannote/speaker-diarization-3.0
     https://huggingface.co/pyannote/segmentation-3.0

2. Clone this repo
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

3. Create your .env file (in the repo root)
   .env contents:
   PYANNOTE_AUTH_TOKEN=<your Hugging Face access token>

4. Build the Docker image
   docker build -t orca:gamma .

5. Run the container
   docker run --rm -it --env-file .env \
     -v "%CD%/PATH_TO_VIDEOS_FOLDER:/app/processmesempai" \
     -v "%CD%/WHERE_TO_SAVE_LOGS:/app/bigtrouble" \
     -v "%CD%/WHERE_IT_SHOULD_SAVE_YOUR_CLIPS:/app/clips" \
     -v "%USERPROFILE%/.cache/huggingface:/root/.cache/huggingface" \
     -v "%USERPROFILE%/.cache/torch:/root/.cache/torch" \
     -e INPUT_FOLDER=/app/processmesempai \
     -e LOG_DIR=/app/bigtrouble \
     -e OUTPUT_FOLDER=/app/clips \
     orca:gamma


Adjust any paths to match your own setup. Good luck