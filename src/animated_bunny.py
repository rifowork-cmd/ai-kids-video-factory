"""Animated original bunny color lesson. No external AI APIs.

Uses Pillow frame rendering and ffmpeg. Silent prototype only.
"""
import argparse
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS = [("#FF6B6B", "RED", "あか"), ("#4D9DE0", "BLUE", "あお"), ("#F9C74F", "YELLOW", "きいろ")]

def font(size, japanese=False):
    paths = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"] if japanese else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def frame(t, lang, w=640, h=360):
    idx = min(int(t // 5), 2)
    local = t - idx * 5
    color, en, ja = COLORS[idx]
    im = Image.new("RGB", (w, h), "#FFF7EA")
    d = ImageDraw.Draw(im)
    # Floating decorations
    for j in range(8):
        x = int((j * 103 + 17 * math.sin(t * 1.3 + j)) % w)
        y = int((j * 79 + 12 * math.cos(t + j)) % h)
        d.ellipse((x-6,y-6,x+6,y+6), fill="#F8DCC9")
    # Bunny hops, waves its ears and blinks
    hop = int(13 * abs(math.sin(t * math.pi * 0.9)))
    ear = int(8 * math.sin(t * 3.0))
    cy = 174 - hop
    d.ellipse((92, 298, 260, 315), fill="#E8DCD2")
    d.ellipse((119+ear,cy-116,155+ear,cy+8), fill="white", outline="#D6C7BE", width=2)
    d.ellipse((195-ear,cy-116,231-ear,cy+8), fill="white", outline="#D6C7BE", width=2)
    d.ellipse((130+ear,cy-104,144+ear,cy-9), fill="#FFC4D4")
    d.ellipse((206-ear,cy-104,220-ear,cy-9), fill="#FFC4D4")
    d.ellipse((102,cy-13,248,cy+133), fill="white", outline="#D6C7BE", width=3)
    blink = (t % 3.3) > 3.12
    if blink:
        d.line((139,cy+55,155,cy+55), fill="#38313A", width=3)
        d.line((194,cy+55,210,cy+55), fill="#38313A", width=3)
    else:
        d.ellipse((141,cy+49,152,cy+62), fill="#38313A")
        d.ellipse((196,cy+49,207,cy+62), fill="#38313A")
    d.ellipse((166,cy+68,185,cy+82), fill="#F2A2A9")
    d.arc((158,cy+78,175,cy+95),0,160,fill="#38313A",width=2)
    d.arc((176,cy+78,193,cy+95),20,180,fill="#38313A",width=2)
    d.ellipse((115,cy+75,137,cy+87), fill="#FFD1DA")
    d.ellipse((212,cy+75,234,cy+87), fill="#FFD1DA")
    # Bouncing ball grows in with easing
    progress = min(1,local/0.7)
    radius = int(48 + 37 * progress)
    bx = 458 + int(13 * math.sin(local * 2.4))
    by = 159 - int(35 * abs(math.sin(local * math.pi * 0.8)))
    d.ellipse((bx-radius,by-radius,bx+radius,by+radius), fill=color, outline="white", width=5)
    # Highlight word
    word = ja if lang == "ja" else en
    f = font(48 if lang == "en" else 42, lang == "ja")
    box = d.textbbox((0,0),word,font=f)
    tw = box[2]-box[0]
    d.rounded_rectangle((335,255,606,331),radius=22,fill="white")
    d.text((470-tw/2,267),word,font=f,fill="#38313A")
    d.text((14,12),f"{idx+1}/3",font=font(22),fill="#756B70")
    return im

def render(lang, output, fps=12):
    if lang not in ("ja","en"):
        raise ValueError("Unsupported language")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        for n in range(15*fps):
            frame(n/fps,lang).save(Path(temp)/f"{n:04d}.png")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                        "-framerate",str(fps),"-i",str(Path(temp)/"%04d.png"),
                        "-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",
                        str(output)],check=True)
    print(output)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--language",choices=["ja","en"],required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    render(args.language,args.output)
