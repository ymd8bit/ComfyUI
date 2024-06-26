FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Variables used at build time.
## CUDA architectures, required by Colmap and tiny-cuda-nn.
## NOTE: All commonly used GPU architectures are included and supported here. To speedup the image build process remove all architectures but the one of your explicit GPU. Find details here: https://developer.nvidia.com/cuda-gpus (8.6 translates to 86 in the line below) or in the docs.
ARG CUDA_ARCHITECTURES=90;89;86;80;75;70;61;52;37

# Set environment variables.
## Set non-interactive to prevent asking for user inputs blocking image creation.
ENV DEBIAN_FRONTEND=noninteractive
## Set timezone as it is required by some packages.
ENV TZ=Asia/Tokyo
## CUDA Home, required to find CUDA in some packages.
ENV CUDA_HOME="/usr/local/cuda"

# Install required apt packages and clear cache afterwards.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    cmake \
    curl \
    wget \
    ffmpeg \
    git \
    sudo \
    vim-tiny \
    libatlas-base-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-program-options-dev \
    libboost-system-dev \
    libboost-test-dev \
    libhdf5-dev \
    libcgal-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libgflags-dev \
    libglew-dev \
    libgoogle-glog-dev \
    libmetis-dev \
    libprotobuf-dev \
    libqt5opengl5-dev \
    libsqlite3-dev \
    libsuitesparse-dev \
    libcairo2-dev \
    qtbase5-dev \
    pkg-config \
    protobuf-compiler \
    python-is-python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-opencv \
    && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
# install pytorch for cuda12
RUN pip install --index-url https://download.pytorch.org/whl/cu121 \
    torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0
# install onnxruntime for cuda12
RUN pip install onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
# install 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
