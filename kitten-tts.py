#!/usr/bin/env python3
"""
KittenTTS wrapper with proper chunking for long text.
Supports --file, --text, and --stdin.

Usage:
    kitten-tts.py --file input.txt output.wav
    kitten-tts.py --text "short text" output.wav
    cat text.txt | kitten-tts.py --stdin output.wav
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

from kittentts import KittenTTS
import soundfile as sf

VOICE_DEFAULT = "Rosie"
SPEED_DEFAULT = 1.5
MODEL_DEFAULT = "KittenML/kitten-tts-nano-0.8"
MAX_CHUNK_SIZE = 1500


def log(msg: str):
    print(f"[kitten-tts] {msg}", file=sys.stderr)


def split_into_chunks(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """Split text into chunks on sentence boundaries."""
    if len(text) <= max_size:
        return [text]

    chunks = []
    current = ""
    sentences = (
        text.replace(". ", ".\n").replace("? ", "?\n").replace("! ", "!\n").split("\n")
    )

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current) + len(sentence) + 2 > max_size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            if current:
                current += " "
            current += sentence
    if current:
        chunks.append(current.strip())

    log(f"Split into {len(chunks)} chunks (max size {max_size})")
    return chunks


def generate_chunk(
    text: str,
    wav_path: Path,
    voice: str = VOICE_DEFAULT,
    speed: float = SPEED_DEFAULT,
    model_name: str = MODEL_DEFAULT,
):
    """Generate audio for one chunk as WAV."""
    tts = KittenTTS(model_name)
    audio = tts.generate(text, voice=voice, speed=float(speed))
    sf.write(wav_path, audio, 24000)
    log("Chunk generated successfully")


def main():
    parser = argparse.ArgumentParser(description="KittenTTS with chunking")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path, help="Input text file")
    group.add_argument("--text", type=str, help="Direct text input")
    group.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("output", type=Path, help="Output .wav file")
    parser.add_argument("--voice", default=VOICE_DEFAULT, help="Voice name")
    parser.add_argument(
        "--speed", type=float, default=SPEED_DEFAULT, help="Speech speed"
    )
    parser.add_argument("--model", default=MODEL_DEFAULT, help="KittenTTS model name")

    args = parser.parse_args()

    if args.file:
        text = args.file.read_text(encoding="utf-8").strip()
        log(f"Read from file: {args.file} ({len(text)} chars)")
    elif args.text:
        text = args.text.strip()
        log(f"Read from --text argument ({len(text)} chars)")
    else:
        text = sys.stdin.read().strip()
        log(f"Read from stdin ({len(text)} chars)")

    if not text:
        log("ERROR: No text provided")
        sys.exit(1)

    chunks = split_into_chunks(text)

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = args.output.with_name(f"{args.output.stem}_chunk_{i:03d}.wav")
        log(f"Generating chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
        generate_chunk(chunk, chunk_file, args.voice, args.speed, args.model)
        chunk_files.append(chunk_file)

    if len(chunk_files) == 1:
        chunk_files[0].rename(args.output)
        log(f"Single chunk saved to {args.output}")
    else:
        log("Concatenating chunks...")
        concat_list = args.output.with_suffix(".txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for fpath in chunk_files:
                f.write(f"file '{fpath}'\n")

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(args.output),
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        for f in chunk_files:
            f.unlink()
        concat_list.unlink()

        log(f"Final audio saved to {args.output} ({len(chunks)} chunks)")


if __name__ == "__main__":
    main()
