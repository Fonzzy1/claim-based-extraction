#!/bin/bash

# --- Function to define dc based on GPU availability ---
setup_dc() {
  if command -v nvidia-smi > /dev/null; then
    dc() {
      docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml -f docker-compose-gpu.yml "$@"
    }
  else
    dc() {
      docker compose -f docker-compose.yml -f ./db/docker-compose.yml -f docker-compose-db-overide.yml "$@"
    }
  fi
}

# --- Run initial setup tasks (one-time) ---
setup_once() {
  [ "$SYS_DIR" = "" ] && export SYS_DIR=$PWD
  echo "Checking for client.json..."
  if [ -f client.json ]; then
    echo "✅ client.json exists"
  else
    echo "❌ client.json does not exist, creating dummy. No drive features availiable"
    touch client.json
  fi

  echo "🔄 Updating git submodules..."
  git submodule update --init --recursive
}

# --- Auto-up logic ---
auto_up() {
  echo "🚀 Running auto 'up'..."

  # Ensure dc is available
  setup_dc

  # Run 'dc up -d' first (in case containers aren't started yet)
  dc up -d

  # Check if Document table is empty
  COUNT=$(dc exec -T db psql -U prisma_user -d prisma_db -t -c 'SELECT count(*) FROM "Document";' 2>/dev/null | xargs)
  if [ $? -ne 0 ] || [ "$COUNT" = "" ]; then
    COUNT=0
  fi

  if [ "$COUNT" -eq 0 ]; then
    echo "⬇️  Database is empty, downloading..."
    dc run download
  else
    echo "✅ Database already filled"
  fi
}

# --- Only run setup and auto_up if being sourced ---
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  setup_once
  setup_dc
  auto_up
else
  echo "❌ Please source this script: 'source $0'"
  exit 1
fi
