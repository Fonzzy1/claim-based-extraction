#! /bin/bash

git submodule update
# Bash script to check if there is an NVIDIA GPU using nvidia-smi.
if command -v nvidia-smi > /dev/null; then
    docker compose -f ./db/docker-compose.yml -f docker-compose.yml -f docker-compose-gpu.yml up --build -d db ollama whisper
else
    docker compose -f ./db/docker-compose.yml -f docker-compose.yml -f docker-compose-gpu.yml up --build -d db whisper
fi

# If db is empty fill it
if docker exec -it postgres psql -U prisma_user -d prisma_db -c "SELECT to_regclass('public.Document');" | grep -q 'Document'; then
    # make sure the download dir credentials are avialiable
    # 
    docker compose -f ./db/docker-compose.yml run download
fi
