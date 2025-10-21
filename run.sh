#! /bin/bash

if [ -f client.json ]; then echo "client.json exists"; else echo "client.json does not exist"; fi

git submodule update

if command -v nvidia-smi > /dev/null; then
  alias dc='docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml -f docker-compose-gpu.yml'
else
  alias dc='docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml'
fi

case "$1" in
    up)
    dc up --build -d
    if [ "$(dc exec -i db psql -U prisma_user -d prisma_db -t -c 'SELECT count(*) FROM "Document";' | xargs)" -eq 0 ]; then
      dc run download
    else
      echo "Database already filled"
    fi
    ;;
down)
    dc down
    ;;
logs)
    dc logs -f
    ;;
  *)
    echo "Usage: $0 {up|down|logs}"
    exit 1
    ;;
esac
