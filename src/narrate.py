"""Generate language-specific voice tracks with edge-tts.

This uses a third-party network-dependent service; it may fail or change.
Review voice quality and provider terms before commercial publishing.
"""
import argparse
import asyncio
from pathlib import Path
import edge_tts

LINES = {
    "ja": ["こんにちは！いっしょに色を覚えよう！", "あか！赤いボールがぴょんぴょん！", "あお！青いボールがころころ！", "きいろ！黄色いボールがジャンプ！", "またあそぼうね！"],
    "en": ["Hello! Let's learn colors!", "Red! The red ball is bouncing!", "Blue! The blue ball is rolling!", "Yellow! The yellow ball jumps!", "See you next time!"],
}
VOICES={"ja":"ja-JP-NanamiNeural","en":"en-US-JennyNeural"}

async def main(lang, output):
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    text=" ".join(LINES[lang])
    await edge_tts.Communicate(text, VOICES[lang], rate="-12%").save(str(output))
    print(output)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--language",choices=LINES,required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    asyncio.run(main(a.language,a.output))
