# DiaGrad research image for the GB10 workstation (NVIDIA GB10, aarch64, CUDA 13.0).
# Base: NGC PyTorch 25.10, pinned by digest. torch stays the NGC build (GB10-capable).
FROM nvcr.io/nvidia/pytorch@sha256:42263b2424fc237b34c4fc4a91c30d603c57eed36e37d31ff6d9a4f1f801edee
COPY requirements.lock /tmp/requirements.lock
RUN pip install --no-cache-dir -r /tmp/requirements.lock
ENV HF_HOME=/hf PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
WORKDIR /repo
