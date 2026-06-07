## Whisper batch transcriber

A minimalist Docker Compose setup to batch-transcribe audio files using OpenAI Whisper and NVIDIA CUDA acceleration.

## Installation & host configuration.

1. Download and install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```bash
sudo apt-get update && sudo apt-get install -y --no-install-recommends \
   ca-certificates \
   curl \
   gnupg2

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

set NVIDIA_CONTAINER_TOOLKIT_VERSION 1.19.1-1
sudo apt-get install -y \
    nvidia-container-toolkit=$NVIDIA_CONTAINER_TOOLKIT_VERSION \
    nvidia-container-toolkit-base=$NVIDIA_CONTAINER_TOOLKIT_VERSION \
    libnvidia-container-tools=$NVIDIA_CONTAINER_TOOLKIT_VERSION \
    libnvidia-container1=$NVIDIA_CONTAINER_TOOLKIT_VERSION
```

2. Configure Docker runtime

Register the NVIDIA runtime extension in Docker's daemon configuration and restart the service.

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

3. Test: `sudo docker run --rm --gpus all --entrypoint python whisper-cuda -c "import torch; print('CUDA verfügbar:', torch.cuda.is_available()); print('Grafikkarte:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Keine')"` should display the following output:

```bash
CUDA verfügbar: True
Grafikkarte: NVIDIA GeForce GTX 1050
```

As an additional test, `sudo docker compose run --rm whisper --help` should display the help of the main transcribe script.

## Configuration

Ensure your directory structure looks like this:

```bash
.
├── Dockerfile
├── docker-compose.yml
└── transcribe.py
```

## Docker Compose Paths

Adjust the local host volume mounts in docker-compose.yml to point to your specific audio folders if needed:

```bash
volumes:
  - home/<username>/Dokumente/Aufnahmen:/in
  - home/<username>/Dokumente/Aufnahmen/Transkriptionen:/out
  ```

## Usage

Hardware Constraint Note: The medium model will trigger a CUDA out of memory error on a 4GB VRAM card (like the GTX 1050). Always explicitly specify `--model small` for stable execution.  
Before running, build the local Python container wrapper (runs on top of PyTorch CUDA runtime): `sudo docker compose build`.

### 1. Batch processing (default mode)

To transcribe all compatible audio files in your input folder at once, simply launch the compose stack without additional arguments. The script will automatically scan the folder and process files sequentially: `sudo docker compose run --rm --entrypoint "python3 transcribe.py" whisper --model small --language de`.

### 2. Transcribing a specific single file

If you want to isolate processing to a single target file, pass the --input flag followed by the path relative to the container's internal /in directory: `sudo docker compose run --rm --entrypoint "python3 transcribe.py" whisper --input "/in/<filename>.m4a" --model small --language de`

### 3. Advanced CLI overrides

You can customize the execution dynamic directly from the command line by tweaking the transcription model or specifying the audio language: `sudo docker compose run --rm whisper --model base --language de --input /in/quick-memo.mp3`.  
Available CLI Arguments:  
- `--input`: Path to a specific file inside /in/ (Omitting this triggers batch mode).
- `--model`: The Whisper model size to use (tiny, base, small, medium, large). Note: smallis highly recommended for 4GB VRAM limitations.
- `--language`: Explicit language code (e.g., de, en). Leaving it out triggers auto-detection.

1. Build the local Python container wrapper (runs on top of PyTorch CUDA runtime): `docker compose build`
2. Process all audio files inside the configured incoming directory (`/in`). This automatically uses the medium model, forces cuda processing, and outputs `.txt` files to `/out`: `docker compose run --rm whisper`.

## Advanced Arguments

Pass any standard script argument overriding the defaults directly to the execution layer:

- Single File: docker compose run --rm whisper --input /in/<filename>.m4a  
- Custom Model: docker compose run --rm whisper --model base
- Change Language: docker compose run --rm whisper --language en
