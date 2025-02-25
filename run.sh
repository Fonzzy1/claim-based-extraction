#! /bin/bash

# Bash script to check if there is an NVIDIA GPU using nvidia-smi.
if command -v nvidia-smi > /dev/null; then
    docker compose up -f docker-compose.yml docker-compose-gpu.yml --build
else
    docker compose up --build
fi
