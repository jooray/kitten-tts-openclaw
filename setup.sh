#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required. Install it first: https://docs.astral.sh/uv/" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required." >&2
  exit 1
fi

uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install --upgrade pip
uv pip install -r requirements.txt

echo "Setup complete."
echo "The KittenTTS model is fetched automatically on first run by the Python wrapper."
