Once upon a time, this folder was an absolute necessity. For some reason I was too stupid to figure out how to get the clipsai package to work at all. I had to manually alter the package scripts to get it to work.

Anyway, it *almost* works on my computer by simply importing clipsai via pip (although package dependency conflicts have given me loads of trouble). 

There are still two scripts that use manual edits: asr.py and editor.py. They belong to the whisperX and clipsai(/media) packages, respectively, and the docker container overwrites the originals during the build.


DONT DEAD OPEN INSIDE may be useful in the future because it contains ffmpeg and yt-dlp. These are FOSS apps, but I'm keeping them here so that maybe everything can be completely self-contained one day. 