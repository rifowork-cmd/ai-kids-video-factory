#!/usr/bin/env python3
import argparse,json,subprocess,urllib.parse,urllib.request,wave
from pathlib import Path
SCRIPTS=[
"日本の最西端、与那国島。その海の底には、巨大な階段のような岩が眠っています。これは自然が作った地形なのでしょうか。それとも、失われた文明の痕跡なのでしょうか。",
"与那国島の近海には、直線的な壁や段差を持つ巨大な海底地形があります。その姿は、まるで古代の神殿のようです。",
"人の手で削ったような形。しかし、規則正しく見えるだけで人工物と証明できるわけではありません。",
"ここからは想像の物語です。もし、はるか昔、この場所に人々が暮らしていたとしたら。彼らはどんな街を築いたのでしょう。",
"岩の割れ目や海の浸食によっても、平らな面や直線的な段差が生まれることがあります。自然はときに、人工物のような姿を作ります。",
"海に沈んだ文明と聞けば、アトランティスを思い浮かべるかもしれません。しかし、与那国島の地形とアトランティスを結ぶ証拠は確認されていません。",
"海底地形は実在します。しかし、それが古代都市だったという結論は確立していません。謎を楽しむことと、事実を見極めること。その両方が大切です。",
"これは自然が生み出した海底の造形なのか。それとも、まだ知られていない歴史への入口なのか。あなたはどう考えますか。"]
def call(url,data=None):
 with urllib.request.urlopen(urllib.request.Request(url,data=data),timeout=90) as r:return r.read()
def main():
 p=argparse.ArgumentParser();p.add_argument('--engine',default='http://127.0.0.1:50021');p.add_argument('--speaker',type=int,default=3);p.add_argument('--images',required=True);p.add_argument('--output',default='yonaguni_narrated.mp4');a=p.parse_args()
 root=Path(a.output).resolve().parent;root.mkdir(parents=True,exist_ok=True);clips=[]
 for i,s in enumerate(SCRIPTS):
  img=Path(a.images)/f'scene_{i:02d}.jpg'
  if not img.exists():raise FileNotFoundError(img)
  q=json.loads(call(a.engine+'/audio_query?'+urllib.parse.urlencode({'text':s,'speaker':a.speaker}),b''));q['speedScale']=0.92
  wav=call(a.engine+'/synthesis?'+urllib.parse.urlencode({'speaker':a.speaker}),json.dumps(q,ensure_ascii=False).encode())
  audio=root/f'narration_{i:02d}.wav';audio.write_bytes(wav)
  with wave.open(str(audio),'rb') as w:duration=w.getnframes()/w.getframerate()+1.2
  clip=root/f'clip_{i:02d}.mp4'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','25','-i',str(img),'-i',str(audio),'-vf','scale=1280:720,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','25','-c:a','aac','-b:a','160k','-t',str(duration),str(clip)],check=True);clips.append(clip)
 manifest=root/'clips.txt';manifest.write_text(''.join("file '"+str(c)+"'\n" for c in clips))
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(Path(a.output).resolve())],check=True)
if __name__=='__main__':main()
