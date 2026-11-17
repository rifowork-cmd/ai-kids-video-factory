"""Create a colorful animal-led silent video prototype from original vector drawings.

No external APIs. Pillow renders scenes; ffmpeg assembles the MP4.
Narration/audio and motion animation are NOT implemented yet.
"""
import argparse
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COLORS = [("#FF6B6B", "RED", "あか"), ("#4D9DE0", "BLUE", "あお"), ("#F9C74F", "YELLOW", "きいろ")]
BG = "#FFF7EA"

def font(size, japanese=False):
    paths = (
        ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
        if japanese else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    )
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_frame(color, english, japanese, lang, path, index, width=1280, height=720):
    image = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(image)
    # Decorative background shapes
    for x, y, r in [(120, 110, 52), (1140, 140, 65), (1060, 590, 38), (240, 620, 35)]:
        d.ellipse((x-r, y-r, x+r, y+r), fill="#FCE4C9")
    # Friendly bunny with original geometric design
    d.ellipse((320, 70, 420, 340), fill="#FFFFFF", outline="#D5C9C0", width=5)
    d.ellipse((465, 70, 565, 340), fill="#FFFFFF", outline="#D5C9C0", width=5)
    d.ellipse((350, 105, 390, 300), fill="#FFC4D4")
    d.ellipse((495, 105, 535, 300), fill="#FFC4D4")
    d.ellipse((280, 225, 610, 560), fill="#FFFFFF", outline="#D5C9C0", width=6)
    d.ellipse((360, 365, 383, 392), fill="#34313A")
    d.ellipse((503, 365, 526, 392), fill="#34313A")
    d.ellipse((420, 410, 470, 445), fill="#F2A2A9")
    d.arc((408, 424, 446, 467), 5, 170, fill="#34313A", width=4)
    d.arc((445, 424, 483, 467), 10, 175, fill="#34313A", width=4)
    d.ellipse((310, 425, 365, 458), fill="#FFD1DA")
    d.ellipse((520, 425, 575, 458), fill="#FFD1DA")
    # Large featured color circle and accent stars
    d.ellipse((770, 190, 1130, 550), fill=color, outline="#FFFFFF", width=14)
    for x, y in [(735, 190), (1150, 390), (860, 585)]:
        pts = [(x + math.cos(a * math.pi / 5 - math.pi / 2) * (30 if a % 2 == 0 else 14),
                y + math.sin(a * math.pi / 5 - math.pi / 2) * (30 if a % 2 == 0 else 14)) for a in range(10)]
        d.polygon(pts, fill="#F7B64A")
    word = japanese if lang == "ja" else english
    label_font = font(90 if lang == "en" else 82, lang == "ja")
    bbox = d.textbbox((0, 0), word, font=label_font)
    text_width = bbox[2] - bbox[0]
    d.rounded_rectangle((685, 575, 1215, 690), radius=35, fill="#FFFFFF")
    d.text((950-text_width/2, 582), word, font=label_font, fill="#34313A")
    d.text((45, 30), f"{index}/3", font=font(36), fill="#6E6571")
    image.save(path)

def render(output, lang):
    if lang not in ("ja", "en"):
        raise ValueError("Language must be ja or en")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        images = []
        for i, (color, english, japanese) in enumerate(COLORS, 1):
            path = Path(tmp) / f"scene{i}.png"
            draw_frame(color, english, japanese, lang, path, i)
            images.append(path)
        # Loop each illustrated card for 5 seconds.
        args = []
        for path in images:
            args.extend(["-loop", "1", "-framerate", "24", "-t", "5", "-i", str(path)])
        filters = "".join(f"[{i}:v]format=yuv420p,setsar=1[v{i}];" for i in range(3))
        filters += "[v0][v1][v2]concat=n=3:v=1:a=0[out]"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        *args, "-filter_complex", filters, "-map", "[out]",
                        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(output)], check=True)
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=["ja", "en"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    render(args.output, args.language)
