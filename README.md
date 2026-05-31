## General

Build a Docker image that installs a version of PyTorch compatible with my GPU.

## Preparations

1. Download and install the [CUDA Toolkit 13.3](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Debian&target_version=13&target_type=deb_local):
```bash
wget https://developer.download.nvidia.com/compute/cuda/13.3.0/local_installers/cuda-repo-debian13-13-3-local_13.3.0-610.43.02-1_amd64.deb
sudo dpkg -i cuda-repo-debian13-13-3-local_13.3.0-610.43.02-1_amd64.deb
sudo cp /var/cuda-repo-debian13-13-3-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-13-3
```

2. Download and install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):
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

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

3. Test: `sudo docker run --rm --gpus all --entrypoint python whisper-cuda -c "import torch; print('CUDA verfügbar:', torch.cuda.is_available()); print('Grafikkarte:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Keine')"` should display the following output:
```bash
CUDA verfügbar: True
Grafikkarte: NVIDIA GeForce GTX 1050
```

