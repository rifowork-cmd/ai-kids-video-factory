#!/usr/bin/env python3
"""Low-cost prototype editor. Requires FFmpeg and FFprobe on PATH."""
import argparse
import json
import subprocess
from pathlib import Path

def run(args):
    subprocess.run(args, check=True)

def duration(path):
    result = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(path)], text=True)
    return float(json.loads(result)["format"]["duration"])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",default="output/prototype.mp4")
    p.add_argument("--seconds",type=int,default=30)
    p.add_argument("--audio",default=None)
    args=p.parse_args()
    source=Path(args.input)
    if not source.is_file(): p.error("Input video not found")
    if args.seconds<1 or args.seconds>120: p.error("Seconds must be 1..120")
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    # Looping is a technical prototype only; it does not invent new scenes.
    command=["ffmpeg","-y","-stream_loop","-1","-i",str(source)]
    if args.audio:
        if not Path(args.audio).is_file(): p.error("Audio file not found")
        command+=["-stream_loop","-1","-i",args.audio]
    command+=["-t",str(args.seconds),"-map","0:v:0"]
    if args.audio: command+=["-map","1:a:0","-c:a","aac","-b:a","160k"]
    else: command+=["-map","0:a?","-c:a","aac"]
    command+=["-vf","scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","23","-movflags","+faststart",str(out)]
    run(command)
    print(f"Created {out} ({duration(out):.1f}s)")

if __name__=="__main__": main()
