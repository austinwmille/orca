# Use Python 3.9 slim as the base image.
FROM python:3.9-slim

# Install system dependencies (ffmpeg and ffprobe are essential).
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libmagic1 \
    libmagic-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file.
COPY requirements.txt ./

# Upgrade pip and install Python dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy patched asr.py into the container
COPY cliaenv/asr.py /tmp/patched_asr.py

# Overwrite the installed whisperx/asr.py
RUN cp /tmp/patched_asr.py \
     "$(python3 -c 'import whisperx, os; print(os.path.dirname(whisperx.__file__))')/asr.py"

# clean up
RUN rm /tmp/patched_asr.py

# Copy the rest of the project into the container.
COPY . .

# Expose any ports required for OAuth; for example, port 8080.
EXPOSE 8080

# Set an environment variable to prevent buffering.
ENV PYTHONUNBUFFERED=1

# Command to run your ctrx script.
CMD ["python", "orca.py"]
