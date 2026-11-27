"""Frase del día sobre fondo en vídeo (estilo del perfil de @club.soberana).
Uso: python3 frase_video.py '{"fondo":"03_jarron","pequeno":["línea 1","línea 2"],"grande":["palabra."],"orden":"pequeno_arriba"|"grande_arriba","salida":"frase-2026-12-03.mp4"}'
Opcional: "bloques":[["p",[..]],["g",[..]],["p",[..]]] (orden libre), "video"/"audio" (fondo propio, p. ej. animar/lentos/AAAA-MM-DD.mp4), "y" (altura del texto).
Fondos (fondos-frase/lentos/NN_nombre.mp4 + .m4a): 16 s seguidos a cámara lenta, sin bucle ni retroceso.
El texto va arriba a la izquierda; marrón en fondos claros y crema en los de color (se decide solo).
"""
import sys, json, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI=os.path.dirname(os.path.abspath(__file__))
W,H=1080,1920
FT=os.path.join(AQUI,'fuentes','Lora-SemiBold.ttf')
FS=os.path.join(AQUI,'fuentes','SourceSans-SemiBold.ttf')
def font(p,s,peso=None):
    return ImageFont.truetype(p,s)
def overlay(frame, pequeno, grande, orden, out, x=90, y=300, bloques=None):
    bg=Image.open(frame).convert('L').resize((W,H))
    reg=bg.crop((x,y,x+800,y+420)); lum=sum(reg.get_flattened_data() if hasattr(reg,'get_flattened_data') else reg.getdata())/(800*420)
    claro=lum>150
    c1=(74,46,20) if claro else (250,240,228); c2=(131,98,64) if claro else (255,248,238)
    fs=font(FS,50,600); fb=font(FT,112,600); fh=font(FS,36,600)
    items=[]; yy=y
    if not bloques:
        bloques=[('p',pequeno),('g',grande)] if orden!='grande_arriba' else [('g',grande),('p',pequeno)]
    for i,(k,lineas) in enumerate(bloques):
        for l in lineas:
            f,c,paso=(fs,c1,66) if k=='p' else (fb,c2,128)
            items.append((l,f,c,yy)); yy+=paso
        yy+=14
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    m=Image.new('L',(W,H),0); dm=ImageDraw.Draw(m)
    for t,f,c,y0 in items:
        tw=dm.textlength(t,font=f); dm.rounded_rectangle((x-30,y0-10,x+tw+30,y0+f.size*1.25),radius=30,fill=90 if claro else 70)
    m=m.filter(ImageFilter.GaussianBlur(40))
    halo=(250,244,236) if claro else (20,14,10)
    sh=Image.new('RGBA',(W,H),halo+(0,)); sh.putalpha(m); im=Image.alpha_composite(im,sh); d=ImageDraw.Draw(im)
    for t,f,c,y0 in items: d.text((x,y0),t,font=f,fill=c+(255,))
    d.text((x,1700),'@club.soberana',font=fh,fill=c1+(255,))
    im.save(out)
def main(a):
    v=a.get('video') or os.path.join(AQUI,'lentos',a['fondo']+'.mp4')
    au=a.get('audio') or os.path.join(AQUI,'lentos',a['fondo']+'.m4a')
    t=tempfile.mkdtemp(); fr=os.path.join(t,'f.png'); ov=os.path.join(t,'o.png')
    subprocess.run(['ffmpeg','-v','error','-y','-ss','0.5','-i',v,'-frames:v','1',fr],check=True)
    overlay(fr,a.get('pequeno',[]),a.get('grande',[]),a.get('orden','pequeno_arriba'),ov,y=a.get('y',300),bloques=a.get('bloques'))
    subprocess.run(['ffmpeg','-v','error','-y','-i',v,'-i',au,'-loop','1','-i',ov,'-filter_complex',
      '[2:v]format=rgba,fade=t=in:st=0.4:d=1.2:alpha=1[o];[0:v][o]overlay=0:0:shortest=1,format=yuv420p[v]',
      '-map','[v]','-map','1:a','-shortest','-c:v','libx264','-crf','18','-preset','slow','-c:a','aac','-b:a','160k','-movflags','+faststart',a['salida']],check=True)
    print('OK',a['salida'])
if __name__=='__main__': main(json.loads(sys.argv[1]))
