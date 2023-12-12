FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

# https://github.com/NVIDIA/nvidia-docker/issues/1009#issuecomment-1181312052
RUN rm /etc/apt/sources.list.d/cuda.list

RUN apt-get update
RUN apt-get update && apt-get install -y git
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

# install pytorch and cuda
ARG PYTORCH='2.0.1'
ARG VERSION='torch=='$PYTORCH'.*'
# Example: `cu102`, `cu113`, 'nightly/cu121', etc.
ARG CUDA='nightly/cu121'
RUN python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA

# set working directory
WORKDIR /app

COPY requirements.txt /app
# Install required packages
RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate

# Copies the trainer code to the docker image.
COPY trainer/__init__.py /app/trainer/__init__.py
COPY trainer/train_model.py /app/trainer/train_model.py
COPY trainer/utils.py /app/trainer/utils.py
COPY trainer/params_and_configs.py /app/trainer/params_and_configs.py
COPY trainer/task.py /app/trainer/task.py

# Set up the entry point to invoke the trainer.
ENTRYPOINT ["python3", "-m", "trainer.task"]