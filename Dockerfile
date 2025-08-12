# trying out cuda-enabled pytorch image, with conda to solve dependency and upgrade conflicts
FROM pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsm6 \
        libxext6 \
        libgl1 \
        libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# grab ffmpeg6
RUN conda install -c conda-forge ffmpeg=6 && \
    conda clean --all -y

# Copy requirements first for some (probably) dumb fucking reason. "Better layer caching" is what Deepseek claims
COPY requirements.txt /app/requirements.txt

# now install dependencies with proper CUDA support, BEFORE installing from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    rm -rf ~/.cache/pip

# Set the working directory inside the container
COPY . /app
WORKDIR /app

# Patch whisperx's asr.py
RUN cp /app/cliaenv/asr.py \
     "$(python -c 'import whisperx, os; print(os.path.dirname(whisperx.__file__))')/asr.py"

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

EXPOSE 8080

# Entry point
CMD ["python", "orca.py"]
