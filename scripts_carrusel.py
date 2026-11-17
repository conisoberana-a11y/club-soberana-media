# Carrusel 1080x1350 con fotos de Coni: texto blanco con sombra suave y degradado claro por línea, sin tapar la cara.
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
S='/tmp/claude-0/-home-user/c888c1db-9f14-5a7e-ab63-d7e1b2ccff8e/scratchpad/'
W,H=1080,1350
FONT=S+'fonts/Lora-SemiBold.ttf'; SANS=S+'fonts/SourceSans-SemiBold.ttf'
det=cv2.FaceDetectorYN.create(S+'models/yunet.onnx','',(540,675),0.55,0.3,50)
def crop(path, fy=None):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    return ImageOps.fit(im,(W,H),method=Image.LANCZOS,centering=(0.5,fy if fy is not None else 0.35))
def faces(im):
    a=cv2.cvtColor(np.array(im.resize((540,675))),cv2.COLOR_RGB2BGR)
    _,f=det.detect(a)
    return [] if f is None else [tuple(v*2 for v in x[:4]) for x in f]
def wrap(d,text,f,maxw):
    if '\n' in text: return text.split('\n')
    out=[];cur=''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur);cur=w
    if cur: out.append(cur)
    return out
def slide(spec,out):
    im=crop(spec['foto'],spec.get('fy'))
    d=ImageDraw.Draw(im)
    size=spec.get('size',62); f=ImageFont.truetype(FONT,size); fs=ImageFont.truetype(SANS,44)
    lines=[(l,tuple(spec.get('color',[255,255,255]))) for l in wrap(d,spec['texto'],f,880)]
    if spec.get('dorado'): lines=[(l,(232,168,90)) for l,_ in lines]
    subl=wrap(d,spec['sub'],fs,880) if spec.get('sub') else []
    lh=int(size*1.28); bh=lh*len(lines)+(30+54*len(subl) if subl else 0)
    fz=faces(im)
    cands=[H-110-bh, 110, int(H*0.55)]
    y0=cands[0]
    for y in cands:
        if all(not (y< fy0+fh+20 and y+bh> fy0-20) for (fx,fy0,fw,fh) in fz): y0=y;break
    m=Image.new('L',(W,H),0); dm=ImageDraw.Draw(m)
    yy=y0
    for l,_ in lines:
        wd=dm.textlength(l,font=f); x=(W-wd)/2
        dm.ellipse((x-28,yy-2,x+wd+28,yy+size*1.22),fill=45); yy+=lh
    if subl:
        yy+=30
        for sl in subl:
            sw=dm.textlength(sl,font=fs); x=(W-sw)/2
            dm.ellipse((x-24,yy-2,x+sw+24,yy+54),fill=40); yy+=54
    m=m.filter(ImageFilter.GaussianBlur(20))
    ov=Image.new('RGBA',(W,H),(10,8,7,0)); ov.putalpha(m)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    tx=Image.new('RGBA',(W,H),(0,0,0,0)); dt=ImageDraw.Draw(tx)
    yy=y0
    for l,c in lines:
        wd=dt.textlength(l,font=f); x=(W-wd)/2
        ds.text((x+1,yy+2),l,font=f,fill=(0,0,0,235),stroke_width=3,stroke_fill=(0,0,0,150)); dt.text((x,yy),l,font=f,fill=c); yy+=lh
    if subl:
        dt.line((W/2-60,yy+10,W/2+60,yy+10),fill=(214,178,104,235),width=3); yy+=30
        for sl in subl:
            sw=dt.textlength(sl,font=fs); x=(W-sw)/2
            ds.text((x+1,yy+2),sl,font=fs,fill=(0,0,0,230),stroke_width=2,stroke_fill=(0,0,0,140)); dt.text((x,yy),sl,font=fs,fill=(250,247,240)); yy+=54
    base=im.convert('RGBA'); base=Image.alpha_composite(base,ov); base=Image.alpha_composite(base,sh.filter(ImageFilter.GaussianBlur(3))); base=Image.alpha_composite(base,tx)
    base.convert('RGB').save(out,quality=95)
    print(out, 'caras',len(fz),'y',y0)
cfg=json.load(open(sys.argv[1]))
for i,s in enumerate(cfg['slides'],1): slide(s, f"{cfg['out']}_{i}.jpg")
