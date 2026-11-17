"""Render a no-API-cost silent visual prototype from a storyboard JSON.

Requires ffmpeg on PATH. This is a *silent preview*, not a finished narrated
children's video. Narration and licensed audio will be added in a later phase.
"""
import argparse
import json
import subprocess
from pathlib import Path

PALETTE = ["0xFCE8E6", "0xDCEEFF", "0xFFF3C9", "0xE7F4E4"]

def render(storyboard, output, width=640, height=360, fps=24):
    data = json.loads(Path(storyboard).read_text(encoding="utf-8"))
    scenes = data["scenes"]
    if not scenes or len(scenes) > 30:
        raise ValueError("Expected 1 to 30 scenes")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    filters = []
    inputs = []
    for i, scene in enumerate(scenes):
        duration = float(scene["seconds"])
        if not 1 <= duration <= 30:
            raise ValueError("Scene duration must be between 1 and 30 seconds")
        inputs += ["-f", "lavfi", "-i", f"color=c={PALETTE[i % len(PALETTE)]}:s={width}x{height}:r={fps}:d={duration}"]
        # Geometric illustrations only. Avoids font availability and copyright issues.
        x = int(width * (0.2 + 0.2 * (i % 3)))
        y = int(height * 0.35)
        filters.append(
            f"[{i}:v]drawbox=x={x}:y={y}:w={width//5}:h={height//3}:color=0xFF9A76:t=fill,"
            f"drawbox=x={x+width//16}:y={y+height//12}:w={width//12}:h={height//8}:color=0xFFFFFF:t=fill,"
            f"format=yuv420p,setsar=1[v{i}]"
        )
    filters.append("".join(f"[v{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=1:a=0[out]")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
           "-filter_complex", ";".join(filters), "-map", "[out]",
           "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(output)]
    subprocess.run(cmd, check=True)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(render(args.storyboard, args.output))
