# Reel con la fórmula viral de Coni: vídeo real, texto arriba en recuadro oscuro, lista numerada, CTA y logo.
import sys,json,subprocess,os
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-user/c888c1db-9f14-5a7e-ab63-d7e1b2ccff8e/scratchpad/'
W,H=1080,1920
cfg=json.load(open(sys.argv[1])); out=cfg['out']; tmp=S+'formula/_'+os.path.basename(out)
FONT=S+'fonts/Lora-SemiBold.ttf'; SANS=S+'fonts/SourceSans-SemiBold.ttf'
GOLD=(232,168,90); WHITE=(255,255,255)
import numpy as np
STYLE=cfg.get('style','degradado')
def box(lines,png,size=62,sub=None,y0=150,align='left',measure=False):
    # Recuadro elegante: fondo oscuro translúcido, filete dorado fino arriba, texto Lora.
    f=ImageFont.truetype(FONT,size); fs=ImageFont.truetype(SANS,46)
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    lh=int(size*1.28); pad=34
    widths=[sum(d.textlength(t,font=f) for t,_ in ln) for ln in lines]
    bw=max(widths)+2*pad; bh=lh*len(lines)+2*pad-12
    subl=[]
    if sub:
        subl=[sub]
        if d.textlength(sub,font=fs)>750-2*pad:
            w_=sub.split(); k=len(w_)//2; subl=[' '.join(w_[:k]),' '.join(w_[k:])]
        bw=max(bw,max(d.textlength(x,font=fs) for x in subl)+2*pad); bh+=40+56*len(subl)
    if measure: return bw,bh
    x0=130 if align=='left' else (int(880-bw) if align=='right' else int(130+(750-bw)/2))
    if STYLE=='recuadro':
        d.rounded_rectangle((x0,y0,x0+bw,y0+bh),radius=18,fill=(18,14,12,150))
        d.line((x0+pad,y0+12,x0+pad+90,y0+12),fill=(214,178,104,230),width=3)
    else:
        # Degradado solo detrás del texto: mancha oscura de bordes muy suaves, del tamaño del bloque de texto.
        from PIL import ImageFilter
        m=Image.new('L',(W,H),0); dm=ImageDraw.Draw(m)
        dm.rounded_rectangle((x0+pad-16,y0+pad-12,x0+bw-pad+16,y0+bh-pad+16),radius=22,fill=170)
        m=m.filter(ImageFilter.GaussianBlur(11))
        im=Image.new('RGBA',(W,H),(10,8,7,0)); im.putalpha(m); d=ImageDraw.Draw(im)
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); dt=ImageDraw.Draw(txt)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    y=y0+pad-2
    for ln,wd in zip(lines,widths):
        x=x0+pad if align in ('left','right') else x0+(bw-wd)/2
        for t_,c in ln:
            ds.text((x+2,y+3),t_,font=f,fill=(0,0,0,200)); dt.text((x,y),t_,font=f,fill=tuple(c)); x+=dt.textlength(t_,font=f)
        y+=lh
    if sub:
        cx=x0+bw/2 if align=='center' else x0+pad+60
        dt.line((cx-60,y+10,cx+60,y+10),fill=(214,178,104,235),width=3)
        yy=y+30
        for sl in subl:
            sx=x0+pad if align in ('left','right') else x0+(bw-dt.textlength(sl,font=fs))/2
            ds.text((sx+2,yy+3),sl,font=fs,fill=(0,0,0,200)); dt.text((sx,yy),sl,font=fs,fill=(250,247,240)); yy+=56
    from PIL import ImageFilter
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(4))); im=Image.alpha_composite(im,txt)
    im.save(png)

import numpy as np, cv2
_DET=None
def faces_at(clip,src_t,zoom=1.0):
    global _DET
    if _DET is None:
        _DET=cv2.FaceDetectorYN.create(S+'models/yunet.onnx','',(540,960),0.55,0.3,50)
    vf=f"scale={int(W*zoom)}:{int(H*zoom)}:force_original_aspect_ratio=increase,crop={W}:{H},scale=540:960"
    isimg=clip.lower().endswith(('.jpg','.jpeg','.png','.webp'))
    r=subprocess.run(['ffmpeg','-nostdin','-v','error']+([] if isimg else ['-ss',f'{src_t:.3f}'])+['-i',clip,'-frames:v','1','-vf',vf,'-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True)
    if len(r.stdout)!=540*960*3: return []
    img=np.frombuffer(r.stdout,np.uint8).reshape(960,540,3)
    _,f=_DET.detect(img)
    return [] if f is None else [tuple(v*2 for v in x[:4]) for x in f]
def face_zone(s,a,b):
    sp=s.get('speed',1.0); boxes=[]
    n=max(4,int((b-a)/0.15))
    for k in range(n+1):
        tr=a+(b-a)*k/n
        for (x,y,w,h) in faces_at(s['clip'],s.get('ss',0)+tr*sp,s.get('zoom',1.0)):
            boxes.append((x-0.45*w,y-0.75*h,x+1.45*w,y+1.35*h))
    if not boxes: return None
    return (min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
def fit(o,size):
    sz=size
    while sz>34:
        bw,bh=box(o['lines'],None,sz,o.get('sub'),0,'left',measure=True)
        if bw<=750: return sz,bw,bh
        sz-=2
    return sz,bw,bh
def place(o,s,a,b):
    size=o.get('size',62)
    fz=face_zone(s,a,b)
    cands=[(270,'left'),(270,'center'),(270,'right'),(360,'left'),(360,'right'),(1300,'center'),(1200,'center'),(1100,'center'),(1000,'center'),(1300,'left'),(1300,'right')]
    sz0,_,_=fit(o,size)
    for sz in (sz0,int(sz0*0.9),int(sz0*0.8)):
        bw,bh=box(o['lines'],None,sz,o.get('sub'),0,'left',measure=True)
        for y,al in cands:
            x0=130 if al=='left' else (880-bw if al=='right' else 130+(750-bw)/2)
            r=(x0-10,y-10,x0+bw+10,y+bh+10)
            if y+bh>1500: continue
            if fz is None or r[2]<fz[0] or r[0]>fz[2] or r[3]<fz[1] or r[1]>fz[3]:
                return sz,y,al,fz
    return sz0,270,'center',fz

segs=cfg['segments']  # each: clip, ss, d, speed, text(lines spec), sub
ins=[];fc=[];ov=[]
t=0
for i,s in enumerate(segs):
    sp=s.get('speed',1.0); dur=s['d']/sp
    z=s.get("zoom",1.0)
    if s['clip'].lower().endswith(('.jpg','.jpeg','.png','.webp')):
        # foto: zoom lento y suave (Ken Burns) para que tenga movimiento
        ins+=['-loop','1','-framerate','30','-t',str(s['d']),'-i',s['clip']]
        nf=int(s['d']*30)
        fc.append(f"[{i}:v]scale={2*W}:{2*H}:force_original_aspect_ratio=increase:flags=lanczos:in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,crop={2*W}:{2*H},zoompan=z='1+0.06*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,unsharp=5:5:0.4:5:5:0.0{(','+s['fx']) if s.get('fx') else ''},format=yuv420p,setsar=1[c{i}]")
        s['_t0']=t; s['_dur']=s['d']; t+=s['d']; continue
    ins+=['-ss',str(s.get('ss',0)),'-t',str(s['d']),'-i',s['clip']]
    fc.append(f"[{i}:v]setpts=PTS/{sp},scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},unsharp=5:5:0.55:5:5:0.0,fps=30,format=yuv420p,setsar=1[c{i}]")
    s['_t0']=t; s['_dur']=dur; t+=dur
n=len(segs)
fc.append(''.join(f'[c{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[base]')
cur='base'; k=n
for i,s in enumerate(segs):
    for j,o in enumerate(s.get('overlays',[])):
        png=S+f"formula/ov_{i}_{j}.png"
        a0=o.get('from',0); b0=o.get('to',s['_dur'])
        if o.get('auto',True):
            sz,yy,al,fz=place(o,s,a0,b0); print(f'seg{i} ov{j}: face={None if fz is None else tuple(int(v) for v in fz)} -> y={yy} {al} size={sz}')
        else:
            sz,_,bh=fit(o,o.get('size',62)); yy=min(max(o.get('y',270),270),1500-bh); al=o.get('align','left')
        box(o['lines'],png,sz,o.get('sub'),yy,al)
        ins+=['-loop','1','-t',f"{t:.2f}",'-i',png]
        a=s['_t0']+o.get('from',0); b=s['_t0']+o.get('to',s['_dur'])
        fc.append(f"[{cur}][{k}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{k}]"); cur=f'v{k}'; k+=1
# logo end card
L=cfg.get('logo_secs',3.0)
ins+=['-loop','1','-t',str(L),'-i',cfg['logo']]
fc.append(f"[{k}:v]scale={W}:{H},fps=30,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.4[lg]")
fc.append(f"[{cur}][lg]concat=n=2:v=1:a=0,format=yuv420p[v]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-nostdin',*ins,'-filter_complex',';'.join(fc),'-map','[v]','-an','-c:v','libx264','-preset','slow','-crf','16','-profile:v','high','-level','4.2','-maxrate','14M','-bufsize','28M','-tune','film','-g','60','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',out],check=True)
print(out, round(t+L,1))
