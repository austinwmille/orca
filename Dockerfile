# Use Python 3.11 slim as the base image.
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg \
      libavutil-dev \
      libavcodec-dev \
      libavformat-dev \
      libavfilter-dev \
      libavdevice-dev \
      libswscale-dev \
      libswresample-dev \
      libsm6 \
      libxext6 \
      libmagic1 \
      libmagic-dev \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Patch whisperx's asr.py
COPY cliaenv/asr.py /tmp/patched_asr.py
RUN cp /tmp/patched_asr.py \
     "$(python3 -c 'import whisperx, os; print(os.path.dirname(whisperx.__file__))')/asr.py" && \
    rm /tmp/patched_asr.py

# Copy the rest of the project into the container.
COPY . .

# env line for unbuffered logs & port 8080 for oauth
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Command to run your ctrx script.
CMD ["python", "orca.py"]
