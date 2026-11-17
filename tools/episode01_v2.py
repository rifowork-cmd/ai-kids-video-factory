#!/usr/bin/env python3
"""Episode 01 V2: source-video recut preview. No claim of newly generated factual footage."""
import argparse, json, subprocess, pathlib, sys
SCENES=[
(0,5,"海底の巨大な階段？"),(5,18,"日本の最西端・与那国島"),
(18,35,"海底に広がる不思議な地形"),(35,50,"人工物に見える段差"),
(50,70,"もし古代文明があったなら？"),(70,90,"自然の作用という説明も"),
(90,105,"人が造った？ 自然が生んだ？"),(105,115,"あなたはどう思う？")]
def run(cmd): subprocess.run(cmd,check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--output",default="episode01_v2_preview.mp4");p.add_argument("--font",default="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc");a=p.parse_args()
 src=pathlib.Path(a.source);out=pathlib.Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 if not src.is_file(): sys.exit("Source video not found: "+str(src))
 if not pathlib.Path(a.font).exists(): sys.exit("Japanese font not found: "+a.font)
 duration=float(json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(src)]))["format"]["duration"])
 if duration<115:sys.exit("Source must be at least 115 seconds")
 filters=[];labels=[]
 for i,(start,end,title) in enumerate(SCENES):
  # Reframe modestly to change the visual rhythm without inventing footage.
  zoom=1.0 if i%3==0 else (1.07 if i%3==1 else 1.13)
  w=int(960/zoom)//2*2;h=int(540/zoom)//2*2
  x="(iw-ow)/2" if i%2==0 else "(iw-ow)*0.35"
  y="(ih-oh)/2"
  escaped=title.replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
  filters.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,fps=30,scale=960:540,crop={w}:{h}:{x}:{y},scale=1280:720,drawbox=x=0:y=590:w=iw:h=110:color=black@0.55:t=fill,drawtext=fontfile='{a.font}':text='{escaped}':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=625,setsar=1[v{i}]")
  labels.append(f"[v{i}]")
 filters.append("".join(labels)+f"concat=n={len(labels)}:v=1:a=0[v]")
 cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(src),"-filter_complex",";".join(filters),"-map","[v]","-an","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
 run(cmd)
 info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height","-of","json",str(out)]))
 sec=float(info["format"]["duration"]);v=next(s for s in info["streams"] if s["codec_type"]=="video")
 qc={"video":str(out),"duration_sec":sec,"resolution":[v["width"],v["height"]],"scenes":len(SCENES),"automated_checks":{"duration_110_to_120":110<=sec<=120,"resolution_1280x720":v["width"]==1280 and v["height"]==720},"human_review_required":["Narration absent in preview","Source footage repeats; replace with scene-specific verified or labeled AI visuals","Fact checking and footage/music rights","Mobile subtitle readability","Audio mix and sync"]}
 (out.parent/"qc_report.json").write_text(json.dumps(qc,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(qc,ensure_ascii=False,indent=2))
 if not all(qc["automated_checks"].values()):sys.exit(2)
if __name__=="__main__":main()
