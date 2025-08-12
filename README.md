# nips’ orca script (previously named ctr+x)

This program is my attempt at making the [ClipsAI](https://github.com/ClipsAI/clipsai) package work. I don't know if it works for anyone, but for me it definitely doesn't as-posted, and at the very least it has major dependency conflicts. The majority of the main script (orca.py), was what they now call vibe-coded. If that matters to you then suck my dick. Incidentally, everything other than that script and the Dockerfile was written by someone else, so I don't wish to take any credit for this.

Anyway, this application takes a given video file and extracts the audio. Using [WhisperX](https://github.com/m-bain/whisperX) ([arXiv:2303.00747](https://arxiv.org/abs/2303.00747)), it transcribes the audio. It then uses ClipsAI to analyze the transcript in an attempt to determine shifts in topic and segments which could function as stand-alone, coherent clips ([ClipsAI reference](https://www.clipsai.com/references/clip), [arXiv:2106.12978](https://arxiv.org/abs/2106.12978)). After this, it performs diarization using [Pyannote Audio](https://github.com/pyannote/pyannote-audio) to determine speakers in the audio file. This data is stored in a dictionary containing speaker_number and timestamps. This can be a very large dictionary depending on the size and content of the given video. 

It takes some number of let's say "screenshots" of the video to determine the position of the speaker(s) during the aforementioned timestamps. It will then use ffmpeg to cut this clips from the main video, and then crop the aspect ratio down to 9x16 (social-media size) while using the position es to keep the speaker in the frame. This is as opposed to cropping arbitrarily.

And that's all. As you can tell, I am not at all sure of the details, honestly. Please see the arxiv papers or literally anyone else for greater insight.

---

## How It Works (again)
> After cloning this repo, you put an .mp4 file in the "processmesempai" folder. Now run orca.py from the root folder. The script will transcribe the video and perform 'diarization' to determine which timestamps of the audio could function as their own short clips. E.g., if you give it a video of a comedy show, it will create timestamps of the beginning and end of each separate joke. 

> Let's take the first timestamp section it finds as an example. It will take some number of low-res "screeshots" of the video in this time range to determine the position of faces in the video. With these two pieces of imformation (the timestamps and the face positions) it will use ffmpeg to:

> 1. Trim the video into clips via the timestamps  
> 2. Resize each clip to a given aspect ratio, keeping the speaker in frame

It’s pretty awesome that it works at all. And after playing with it a lot it works pretty well actually, so don't give up.

I am certain that some of the particulars above are incorrect, but it gives a decent understanding to start and will give some basic insight when it inevitably breaks.

---

## Use Cases & Caveats

- **Ideal for:** Podcasts, long interviews, panel discussions, and similar formats.  
- **Less ideal for:** Wide-shot scenes with many faces (e.g., speeches to a crowd), since face-centering may fail and the speaker dictionaries will be extravagantly large. Also, apparently, it's very bad for recorded video game tournaments. It correctly finds the coherent clips AND the faces, but the faces are usually the players' faces at the bottom corners so it crops the video toward the edges, instead of to the center where the action is taking place.  
- **Resource notes:** It can and will use a large amount of memory. This is the biggest factor in its crashes that I've noticed. To combat this, cut the video into smaller segments instead of feeding the entire video.

Almost the entirety of the work can be found at (clipsai.com). clipsai is an open source python package literally made to do this. I had a ton of trouble getting it to work as-posted, which is why I am putting this here at all, and I don't think there has been an update in over a year. If you follow the (only 4 or 5) lines in the quickstart section of that repo you run into dependency conflicts immediately. whisperx has had much more development than the clipsai package which I believe is related to the problem. Anyway, what it needed was dockerization, which is the real key of this project here. Lastly, if you're reading this then I highly suggest you research other packages and applications to do this better and more efficiently than this one. I am sure one is out there somewhere.

## Quickstart Instructions

These steps guide you through setup. You will need to request access to certain gated models on Hugging Face.

1. **Create a Hugging Face account & request model access**  
   - **Definitely Required:**  
     - https://huggingface.co/pyannote/segmentation  
     - https://huggingface.co/pyannote/speaker-diarization-3.1
   - **Probably also required** (I'd just do all of them):  
     - https://huggingface.co/pyannote/speaker-diarization
     - https://huggingface.co/pyannote/speaker-segmentation  
     - https://huggingface.co/pyannote/speaker-diarization-3.0  
     - https://huggingface.co/pyannote/segmentation-3.0  

2. **Clone this repo**  
   ```bash
   git clone https://github.com/austinwmille/orca.git
   cd orca
   ```

3. **Create your `.env` file** (in the repo root)  
   ```
   PYANNOTE_AUTH_TOKEN=<your Hugging Face access token>
   ```

4. **Build the Docker image**  
   ```bash
   docker build -t orca:someTAGhere .
   ```
5. **Put a test video in the "processmesempai" folder**  
   
6. **Run the container**  
   ```bash
   docker run --rm -it --gpus all \
     --env-file .env \
     -v "%CD%/processmesempai:/app/processmesempai" \
     -v "%CD%/bigtrouble:/app/bigtrouble" \
     -v "%CD%/clips:/app/clips" \
     -e NVIDIA_VISIBLE_DEVICES=all \
     -e INPUT_FOLDER=/app/processmesempai \
     -e LOG_DIR=/app/bigtrouble \
     -e OUTPUT_FOLDER=/app/clips \
     orca:someTAGhere
   ```

If something fails check the "bigtrouble" folder! Every run produces a log which is saved there. Try giving the log to your favorite LLM and see what it says. Good luck!

Oh, yeah, I run this on Linux using an Nvidia GPU. If you have something other than that you may have to make adjustments. For example, on Windows I used to use "%CD%" like above, but now I use "${PWD}", like below. Also, if you have NO GPU the script should still run. At least, it used to for me. Lastly, if you have an AMD or Intel GPU then you may need to make adjustments to allow the docker container to utilize it. Actually, now that I say that idk if you'll see ANY speedup on those cards due to the absence of CUDA. It may just have to run on CPU only :( 

--

---

## Docker Run Example

> *My current line to run the Docker container:*

```bash
docker run --rm -it --gpus all \
  --env-file .env \
  -v "${PWD}/processmesempai:/app/processmesempai" \
  -v "${PWD}/bigtrouble:/app/bigtrouble" \
  -v "${PWD}/clips:/app/clips" \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e INPUT_FOLDER=/app/processmesempai \
  -e LOG_DIR=/app/bigtrouble \
  -e OUTPUT_FOLDER=/app/clips \
  orca:epsilon
```

---

If you have trouble with this or would like updates (or maybe are wondering why so much trash is loaded by default) please keep in mind that aside from a base-model Macbook Air (2014) running debianOS, the entirety of this development work (and the script itself) was done and run on the following machine:

![image](https://github.com/user-attachments/assets/7c3bd146-dce0-44f7-981d-3f4b5e5b0b99).

