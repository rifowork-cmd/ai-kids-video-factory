"""Create a non-destructive reframing preview from an existing narrated video.

Requires FFmpeg. Audio stays on the original timeline. This is not a substitute
for adding varied, properly licensed footage or checking subtitle timing.
"""
import argparse
import subprocess
from pathlib import Path


def render(source: Path, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "scale=1440:810:flags=lanczos,"
        "crop=1280:720:"
        "x='(in_w-out_w)*(0.5+0.25*sin(2*PI*t/28))':"
        "y='(in_h-out_h)*(0.5+0.20*cos(2*PI*t/28))',"
        "setsar=1,format=yuv420p"
    )
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-vf", vf, "-map", "0:v:0", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "copy", "-movflags", "+faststart", str(output)
    ], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(args.input, args.output)
