# kitten-tts-openclaw

## No longer maintained

I do not maintain this project any more. For turning text into audio see
[markdown2audio](https://github.com/jooray/markdown2audio). For local speech
recognition rather than synthesis, see
[Livecaster](https://github.com/jooray/livecaster-llm).

For what I am building now, see my
[project showcase](https://juraj.bednar.io/showcase/).

I also write books and work on things that are not code: my cypherpunk novel
[Tamers of Entropy](https://tamersofentropy.net/), my English podcast
[Option Plus](https://optionplus.io/), [my blog](https://juraj.bednar.io/en/blog-en/),
and [everything else](https://juraj.bednar.io/en). There is also
[more about me](https://juraj.bednar.io/en/about-me/).

A small wrapper around KittenTTS for local text-to-speech on low-power machines.

It is meant for the boring, practical use case: take text, generate speech locally, and get a WAV file you can use in other workflows. It runs in a `uv`-managed virtual environment, supports long text, and stays CPU-friendly.

## What it does

- Generates speech from text using `KittenML/kitten-tts-nano-0.8`
- Runs on CPU-only machines
- Supports `--text`, `--file`, and `--stdin`
- Splits long text into chunks and joins them back into a single WAV
- Writes 24 kHz WAV output

## Files

- `setup.sh` - creates the virtualenv and installs dependencies
- `kitten-tts.sh` - shell entrypoint
- `kitten-tts.py` - chunking and generation logic
- `requirements.txt` - pinned Python dependencies
- `test-kitten-tts.py` - simple smoke test

## Requirements

System packages:

- Python 3.12
- `uv`
- `ffmpeg` for joining multiple WAV chunks, and optionally converting WAV to M4A

The model does not need a separate manual download. It is fetched automatically on first run when `KittenTTS("KittenML/kitten-tts-nano-0.8")` initializes.

## Setup

```bash
git clone https://github.com/jooray/kitten-tts-openclaw
cd kitten-tts-openclaw
./setup.sh
```

That creates `.venv`, installs the pinned dependencies, and leaves the wrapper ready to use.

## Usage

### Short text

```bash
./kitten-tts.sh --text "Hello world" out.wav
```

### File input

```bash
./kitten-tts.sh --file input.txt out.wav
```

### stdin input

```bash
cat input.txt | ./kitten-tts.sh --stdin out.wav
```

For longer input, prefer `--stdin` or `--file` instead of stuffing everything into a shell argument.

### Voice and speed

```bash
./kitten-tts.sh --text "Hello world" out.wav --voice Rosie --speed 1.6
```

## Notes

- Default voice: `Rosie`
- Default speed: `1.5`
- Default model: `KittenML/kitten-tts-nano-0.8`
- Output format: WAV at 24 kHz
- The wrapper sets `PHONEMIZER_ESPEAK_LIBRARY` and `ESPEAK_DATA_PATH` before starting Python, so no site-packages patching is needed in this public version

If your chat platform wants AAC/M4A voice messages, convert the WAV afterward:

```bash
ffmpeg -i out.wav -c:a aac -b:a 32k -ar 16000 -ac 1 out.m4a -y
```

## OpenClaw / TOOLS.md example

If you want to document this in an OpenClaw workspace, this is the useful part:

```md
## KittenTTS - text to speech for sending voice messages
- Wrapper: `~/path/to/kitten-tts-openclaw/kitten-tts.sh`
- Venv: `~/path/to/kitten-tts-openclaw/.venv`
- Model: `KittenML/kitten-tts-nano-0.8`
- Voices: Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo (default: Rosie, speed 1.5)
- Input modes: `--text`, `--file`, `--stdin` (prefer `--stdin` or `--file` for long text)
- Output: 24kHz WAV, CPU-only
- Setup: `cd ~/path/to/kitten-tts-openclaw && ./setup.sh`
- espeak handling: wrapper sets `PHONEMIZER_ESPEAK_LIBRARY` + `ESPEAK_DATA_PATH`

### Sending voice messages on SimpleX
1. Generate WAV: `cat input.txt | ~/path/to/kitten-tts-openclaw/kitten-tts.sh --stdin /tmp/out.wav --voice Rosie --speed 1.6`
2. Convert to m4a: `ffmpeg -i /tmp/out.wav -c:a aac -b:a 32k -ar 16000 -ac 1 /tmp/out.m4a -y`
3. Reply with EXACTLY this:
   ```
   [[audio_as_voice]]
   MEDIA:/tmp/out.m4a
   NO_REPLY
   ```
```

## Design

This repo is intentionally plain:

- shell wrapper for environment setup
- Python for chunking and generation
- `uv` for environment management
- automatic model fetch on first run

No Docker, no extra packaging layer, no pretending this needs more machinery than it does.
