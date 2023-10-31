# FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04 
# FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
# FROM nvidia/cuda:12.2.0-runtime-ubuntu20.04
FROM nvidia/cuda:11.4.3-runtime-ubuntu20.04

ENV LANG=C.UTF-8

ENV LC_ALL=C.UTF-8

ENV PYTHONIOENCODING=UTF-8

ENV PYTHONUNBUFFERED=1

ENV NVIDIA_VISIBLE_DEVICES=


# USER root

ENV DEBIAN_FRONTEND=noninteractive
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt set -eux && \
    apt-get update -y && \
    apt-get install -q -y --no-install-recommends --allow-remove-essential \
        ca-certificates gnupg2 bash build-essential ffmpeg libsm6 libxext6 python-is-python3

RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get install -y --no-install-recommends --allow-remove-essential software-properties-common && \
    # add deadsnakes ppa to install python
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends --allow-remove-essential curl python3.9 python3.9-dev python3.9-distutils

RUN ln -sf /usr/bin/python3.9 /usr/bin/python3 && \
    ln -sf /usr/bin/pip3.9 /usr/bin/pip3

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm -rf get-pip.py

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Default port for BentoServer
# EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



