#!/usr/bin/env bash
# KittenTTS wrapper - supports --file, --text, --stdin
# Usage: ./kitten-tts.sh [--file file.txt | --text "text" | --stdin] output.wav [--voice NAME] [--speed FLOAT]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/kitten-tts.py"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Error: virtual environment not found at $SCRIPT_DIR/.venv. Run ./setup.sh first." >&2
    exit 1
fi

export PHONEMIZER_ESPEAK_LIBRARY="$($VENV_PYTHON -c 'import espeakng_loader; print(espeakng_loader.get_library_path())')"
export ESPEAK_DATA_PATH="$($VENV_PYTHON -c 'import espeakng_loader; print(espeakng_loader.get_data_path())')"

exec "$VENV_PYTHON" "$PYTHON_SCRIPT" "$@"
