Once upon a time, this folder was an absolute necessity. For some reason I was too stupid to figure out how to get the clipsai package to work at all. I had to manually alter the package scripts to get it to work.

Anyway, it *almost* works on my computer by simply importing clipsai via pip (although package dependency conflicts have given me loads of trouble). 

There is still one script that uses manual edits: asr.py. It belongs to the whisperX package, and the docker container overwrites the originals during the build.

Still also contained in this folder is editor.py. This belongs to the clipsai(/media) package but is no longer required. I have removed it's overwrite line from the dockerfile, but keeping it for now just in case.

DONT DEAD OPEN INSIDE may be useful in the future because it contains ffmpeg and yt-dlp. These are FOSS apps, but I'm keeping them here so that maybe everything can be completely self-contained one day. 