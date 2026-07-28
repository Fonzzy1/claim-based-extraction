#!/bin/bash

setup_dc() {
  if command -v nvidia-smi > /dev/null; then
      dc() {
      docker compose -f docker-compose.yml -f docker-compose-gpu.yml "$@"
    }
  else
      dc() {
      docker compose -f docker-compose.yml "$@"
    }
  fi
}

setup_once() {
  docker volume inspect ollama >/dev/null 2>&1 || docker volume create ollama
}

auto_up() {
  echo "🚀 Running auto 'up'..."
  setup_dc
  dc build pipeline
}

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  setup_once
  setup_dc
  auto_up
else
  echo "❌ Please source this script: 'source $0'"
  exit 1
fi
