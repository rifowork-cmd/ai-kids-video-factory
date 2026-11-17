"""Generate full Japanese Yonaguni episode narration using edge-tts."""
import asyncio
from pathlib import Path
import edge_tts

SCENES = [
"日本の最西端、与那国島。その海の底には、巨大な階段のような岩が眠っています。これは自然が作った地形なのでしょうか。それとも、失われた文明の痕跡なのでしょうか。",
"与那国島の近海には、直線的な壁や段差を持つ巨大な海底地形があります。その姿は、まるで古代の神殿のようです。",
"人の手で削ったような形。しかし、規則正しく見えるだけで人工物と証明できるわけではありません。",
"ここからは想像の物語です。もし、はるか昔、この場所に人々が暮らしていたとしたら。彼らはどんな街を築いたのでしょう。",
"岩の割れ目や海の浸食によっても、平らな面や直線的な段差が生まれることがあります。自然はときに、人工物のような姿を作ります。",
"海に沈んだ文明と聞けば、アトランティスを思い浮かべるかもしれません。しかし、与那国島の地形とアトランティスを結ぶ証拠は確認されていません。",
"海底地形は実在します。しかし、それが古代都市だったという結論は確立していません。謎を楽しむことと、事実を見極めること。その両方が大切です。",
"これは自然が生み出した海底の造形なのか。それとも、まだ知られていない歴史への入口なのか。あなたはどう考えますか。"
]

async def main():
    out = Path("output/yonaguni_narration")
    out.mkdir(parents=True, exist_ok=True)
    voice = "ja-JP-NanamiNeural"
    for i, text in enumerate(SCENES):
        await edge_tts.Communicate(text, voice, rate="-8%").save(str(out / f"scene_{i:02d}.mp3"))
    (out / "script.txt").write_text("\n\n".join(SCENES), encoding="utf-8")
    print(f"Generated {len(SCENES)} narration segments in {out}")

if __name__ == "__main__":
    asyncio.run(main())
