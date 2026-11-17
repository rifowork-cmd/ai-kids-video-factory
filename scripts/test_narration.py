"""Generate a short Japanese narration sample using OpenAI TTS."""
import os
from pathlib import Path
from openai import OpenAI

key = os.environ.get("OPENAI_API_KEY")
if not key:
    raise SystemExit("OPENAI_API_KEY is not configured")

output = Path("output/narration_sample.mp3")
output.parent.mkdir(parents=True, exist_ok=True)
client = OpenAI(api_key=key)
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="nova",
    input="こんにちは！今日もわくわくする冒険が始まるよ。みんな、一緒に行こう！",
) as response:
    response.stream_to_file(output)
print(f"Created {output}")
