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

# Copy the requirements file and install Python dependencies.
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container.
COPY . .

# Expose any ports required for OAuth; for example, port 8080.
EXPOSE 8080

# Set an environment variable to prevent buffering.
ENV PYTHONUNBUFFERED=1

# Command to run your ctrx script.
CMD ["python", "orca.py"]
