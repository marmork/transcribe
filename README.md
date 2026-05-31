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
  - ~/Dokumente/Aufnahmen:/in
  - ~/Dokumente/Aufnahmen/Transkriptionen:/out
  ```

## Usage

1. Build the local Python container wrapper (runs on top of PyTorch CUDA runtime): `docker compose build`
2. Process all audio files inside the configured incoming directory (`/in`). This automatically uses the medium model, forces cuda processing, and outputs `.txt` files to `/out`: `docker compose run --rm whisper`.

## Advanced Arguments

Pass any standard script argument overriding the defaults directly to the execution layer:

- Single File: docker compose run --rm whisper --input /in/<filename>.m4a  
- Custom Model: docker compose run --rm whisper --model base
- Change Language: docker compose run --rm whisper --language en
