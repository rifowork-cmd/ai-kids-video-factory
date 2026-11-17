"""Generate Japanese documentary narration using OpenAI TTS. Requires OPENAI_API_KEY."""
import argparse
import os
from pathlib import Path
from openai import OpenAI

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", default="atlantis/script.txt")
    p.add_argument("--output", default="output/narration.mp3")
    p.add_argument("--voice", default="onyx")
    args = p.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY secret")
    text = Path(args.script).read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("Script is empty")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    client = OpenAI()
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=args.voice,
        input=text,
        instructions="Japanese. Calm, cinematic mystery-documentary narration. Clear pauses, natural emphasis.",
    ) as response:
        response.stream_to_file(output)
    print(f"Generated {output}")

if __name__ == "__main__":
    main()
