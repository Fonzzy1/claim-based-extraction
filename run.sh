#! /bin/bash

# cp /root/mount/hansard_db_client_secret.json  client.json
if [ -f client.json ]; then echo "client.json exists"; else echo "client.json does not exist"; fi

git submodule update
# Bash script to check if there is an NVIDIA GPU using nvidia-smi.
if command -v nvidia-smi > /dev/null; then
alias dc='docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml -f docker-compose-gpu.yml'
else
alias dc='docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml'
fi
dc up --build -d

# If db is empty fill it
if [ "$(dc exec -it db psql -U prisma_user -d prisma_db -t -c 'SELECT count(*) FROM \"Document\";' | xargs)" -eq 0 ]; then
    # make sure the download dir credentials are avialiable
    dc run download
fi
