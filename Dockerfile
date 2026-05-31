FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir "setuptools<70"
RUN pip install --no-cache-dir --no-build-isolation openai-whisper==20230314

ENTRYPOINT ["whisper"]
