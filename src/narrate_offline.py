"""Generate Japanese and English narration offline with Piper-compatible eSpeak NG fallback.

This is a reliability prototype, not studio-quality narration.
"""
import argparse
import subprocess
from pathlib import Path

LINES={
 "ja": ["こんにちは。いっしょに色を覚えよう。","赤いボール。","青いボール。","黄色いボール。"],
 "en": ["Hello! Let's learn colors!","Red ball.","Blue ball.","Yellow ball."]
}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--language",choices=["ja","en"],required=True)
 p.add_argument("--output",required=True)
 a=p.parse_args()
 dest=Path(a.output)
 dest.parent.mkdir(parents=True,exist_ok=True)
 # espeak-ng is fully offline. The Japanese voice is robotic and needs replacing
 # with a licensed high-quality provider before publication.
 voice="ja" if a.language=="ja" else "en-us"
 text=" ".join(LINES[a.language])
 wav=dest.with_suffix(".wav")
 subprocess.run(["espeak-ng","-v",voice,"-s","125","-w",str(wav),text],check=True)
 if dest.suffix.lower()==".wav":
  print(dest)
 else:
  subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(wav),str(dest)],check=True)
  wav.unlink(missing_ok=True)
  print(dest)
if __name__=="__main__":
 main()
