#! /bin/bash

# Bash script to check if there is an NVIDIA GPU using nvidia-smi.
if command -v nvidia-smi > /dev/null; then
    docker compose -f docker-compose.yml -f docker-compose-gpu.yml up --build
else
    docker compose up --build
fi
