#!/usr/bin/env python3
"""Smoke test for kitten-tts-openclaw."""
import os
import sys
from pathlib import Path

import espeakng_loader
from kittentts import KittenTTS
import soundfile as sf

os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = str(espeakng_loader.get_library_path())
os.environ['ESPEAK_DATA_PATH'] = str(espeakng_loader.get_data_path())

print(f"PHONEMIZER_ESPEAK_LIBRARY={os.environ['PHONEMIZER_ESPEAK_LIBRARY']}")
print(f"ESPEAK_DATA_PATH={os.environ['ESPEAK_DATA_PATH']}")

model = KittenTTS("KittenML/kitten-tts-nano-0.8")
audio = model.generate("Hello world, this is a test.", voice="Rosie", speed=1.5)

output_path = Path("/tmp/kitten-tts-test.wav")
sf.write(output_path, audio, 24000)

if output_path.exists() and output_path.stat().st_size > 0:
    print(f"OK: wrote {output_path} ({output_path.stat().st_size} bytes)")
    sys.exit(0)

print("FAIL: output file missing or empty")
sys.exit(1)
