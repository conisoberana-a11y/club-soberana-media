# Reel con la fórmula viral de Coni: vídeo real, texto arriba en recuadro oscuro, lista numerada, CTA y logo.
import sys,json,subprocess,os
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-user/c888c1db-9f14-5a7e-ab63-d7e1b2ccff8e/scratchpad/'
W,H=1080,1920
cfg=json.load(open(sys.argv[1])); out=cfg['out']; tmp=S+'formula/_'+os.path.basename(out)
FONT=S+'fonts/Lora-SemiBold.ttf'; SANS=S+'fonts/SourceSans-SemiBold.ttf'
GOLD=(232,168,90); WHITE=(255,255,255)
def box(lines,png,size=62,sub=None):
    # lines: list of [(text,color)] segments per line
    f=ImageFont.truetype(FONT,size); fs=ImageFont.truetype(SANS,36)
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    lh=int(size*1.28); pad=34; x0,y0=60,150
    widths=[sum(d.textlength(t,font=f) for t,_ in ln) for ln in lines]
    bw=max(widths)+2*pad; bh=lh*len(lines)+2*pad-12
    if sub: bw=max(bw,d.textlength(sub,font=fs)+2*pad); bh+=56
    d.rounded_rectangle((x0,y0,x0+bw,y0+bh),radius=22,fill=(20,16,14,165))
    y=y0+pad-6
    for ln in lines:
        x=x0+pad
        for t,c in ln: d.text((x,y),t,font=f,fill=tuple(c)); x+=d.textlength(t,font=f)
        y+=lh
    if sub: d.text((x0+pad,y+4),sub,font=fs,fill=(235,228,215))
    # firma
    fh=ImageFont.truetype(SANS,30); d.text((W-60-d.textlength('@club.soberana',font=fh),y0+12),'' ,font=fh)
    im.save(png)
segs=cfg['segments']  # each: clip, ss, d, speed, text(lines spec), sub
ins=[];fc=[];ov=[]
t=0
for i,s in enumerate(segs):
    sp=s.get('speed',1.0); dur=s['d']/sp
    ins+=['-ss',str(s.get('ss',0)),'-t',str(s['d']),'-i',s['clip']]
    fc.append(f"[{i}:v]setpts=PTS/{sp},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},unsharp=5:5:0.55:5:5:0.0,fps=30,format=yuv420p,setsar=1[c{i}]")
    s['_t0']=t; s['_dur']=dur; t+=dur
n=len(segs)
fc.append(''.join(f'[c{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[base]')
cur='base'; k=n
for i,s in enumerate(segs):
    for j,o in enumerate(s.get('overlays',[])):
        png=S+f"formula/ov_{i}_{j}.png"; box(o['lines'],png,o.get('size',62),o.get('sub'))
        ins+=['-loop','1','-t',f"{t:.2f}",'-i',png]
        a=s['_t0']+o.get('from',0); b=s['_t0']+o.get('to',s['_dur'])
        fc.append(f"[{cur}][{k}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{k}]"); cur=f'v{k}'; k+=1
# logo end card
L=cfg.get('logo_secs',3.0)
ins+=['-loop','1','-t',str(L),'-i',cfg['logo']]
fc.append(f"[{k}:v]scale={W}:{H},fps=30,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.4[lg]")
fc.append(f"[{cur}][lg]concat=n=2:v=1:a=0,format=yuv420p[v]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-nostdin',*ins,'-filter_complex',';'.join(fc),'-map','[v]','-an','-c:v','libx264','-preset','slow','-crf','16','-profile:v','high','-level','4.2','-maxrate','14M','-bufsize','28M','-tune','film','-g','60','-movflags','+faststart',out],check=True)
print(out, round(t+L,1))
