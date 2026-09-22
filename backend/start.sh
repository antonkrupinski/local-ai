#!/usr/bin/env bash
set -euo pipefail

# Default port and model path
PORT="${PORT:-8080}"
MODEL_PATH="${LLAMA_MODEL_PATH:-/app/models/ggml-model.bin}"

export LLAMA_MODEL_PATH="$MODEL_PATH"

echo "Starting backend on port $PORT with model path $LLAMA_MODEL_PATH"

exec uvicorn app:app --host 0.0.0.0 --port "$PORT"
