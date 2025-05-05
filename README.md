# nips’ orca script (previously ctr+x)

This application takes a video and extracts the audio. Using [WhisperX](https://github.com/m-bain/whisperX) ([arXiv:2303.00747](https://arxiv.org/abs/2303.00747)), it transcribes the audio. It then uses ClipsAI to analyze the transcript in an attempt to determine shifts in topic and segments which could function as stand-alone, coherent clips ([ClipsAI reference](https://www.clipsai.com/references/clip), [arXiv:2106.12978](https://arxiv.org/abs/2106.12978)). After this, it performs diarization using [Pyannote Audio](https://github.com/pyannote/pyannote-audio) to determine speakers in the audio file. This data is stored in a dictionary containing speaker_number and timestamps.

I am not totally sure what happens next, honestly, and I really don't care at the moment. Please see the arxiv papers or literally anyone else for greater insight.

---

## How It Works (Roughly)
> In practice, after transcription and diarization, the script uses audio cues, changes in content/subject, voice inflections, pauses, arbitrary frames, etc to:

> 1. Trim the video into clips  
> 2. Resize each clip to a given aspect ratio, keeping the speaker in frame

It’s pretty awesome that it works at all. And after playing with it a lot it works pretty well actually, so don't give up.

I am certain that some of the particulars above are incorrect, but it gives a decent understanding to start and will give some insight when it breaks.

---

## Use Cases & Caveats

- **Ideal for:** Podcasts, long interviews, panel discussions, and similar formats.  
- **Less ideal for:** Wide-shot scenes with many faces (e.g., speeches to a crowd), since face-centering may fail and the speaker dictionaries will be extravagantly large.  
- **Resource notes:** It can and will use a large amount of memory. It can and will crash for no reason.

Almost the entirety of the work can be found at (clipsai.com). clipsai is an open source python package literally made to do this. I had a ton of trouble getting it to work as-posted, which is why I am putting this here at all, and I don't think there has been an update in over a year. If you follow the (only 4 or 5) lines in the quickstart section of that repo you run into dependency conflicts immediately. whisperx has had much more development than the clipsai package which I believe is related to the problem.

--

## Quickstart Instructions

These steps guide you through setup. You will need to request access to certain gated models on Hugging Face.

1. **Create a Hugging Face account & request model access**  
   - **Required:**  
     - https://huggingface.co/pyannote/segmentation  
     - https://huggingface.co/pyannote/speaker-diarization-3.1  
   - **Optional** (if you hit missing-model errors):  
     - https://huggingface.co/pyannote/speaker-diarization  
     - https://huggingface.co/pyannote/speaker-segmentation  
     - https://huggingface.co/pyannote/speaker-diarization-3.0  
     - https://huggingface.co/pyannote/segmentation-3.0  

2. **Clone this repo**  
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

3. **Create your `.env` file** (in the repo root)  
   ```
   PYANNOTE_AUTH_TOKEN=<your Hugging Face access token>
   ```

4. **Build the Docker image**  
   ```bash
   docker build -t orca:gamma .
   ```

5. **Run the container**  
   ```bash
   docker run --rm -it --env-file .env      -v "%CD%/processmesempai:/app/processmesempai"      -v "%CD%/bigtrouble:/app/bigtrouble"      -v "%CD%/clips:/app/clips"      -v "%USERPROFILE%/.cache/huggingface:/root/.cache/huggingface"      -v "%USERPROFILE%/.cache/torch:/root/.cache/torch"      -e INPUT_FOLDER=/app/processmesempai      -e LOG_DIR=/app/bigtrouble      -e OUTPUT_FOLDER=/app/clips      orca:gamma
   ```

Adjust any paths to match your own setup. Good luck!

--

---

## Docker Run Example

> *My current line to run the Docker container—edit with your own paths:*

```bash
docker run --rm -it --env-file .env   -v "${PWD}\processmesempai:/app/processmesempai"   -v "${PWD}\bigtrouble:/app/bigtrouble"   -v "${PWD}\clips:/app/clips"   -v "${HOME}\.cache\huggingface:/root/.cache/huggingface"   -v "${HOME}\.cache\torch:/root/.cache/torch"   -e INPUT_FOLDER=/app/processmesempai   -e LOG_DIR=/app/bigtrouble   -e OUTPUT_FOLDER=/app/clips   orca:gamma
```

---
