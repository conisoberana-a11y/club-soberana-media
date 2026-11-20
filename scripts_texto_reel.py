import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S='/tmp/claude-0/-home-user/c888c1db-9f14-5a7e-ab63-d7e1b2ccff8e/scratchpad/'
D=S+'dom/'
W,H=1080,1920
FT=S+'fonts/Lora-SemiBold.ttf'; FS=S+'fonts/SourceSans-SemiBold.ttf'
GOLD=(214,178,120); WH=(255,255,255)
def fit(path,cx=0.5):
    i=Image.open(path).convert('RGB'); w,h=i.size
    if w/h>W/H:
        nw=int(h*W/H); x=int(max(0,min(w-nw,cx*w-nw/2))); i=i.crop((x,0,x+nw,h))
    else:
        nh=int(w*H/W); i=i.crop((0,0,w,nh))
    return i.resize((W,H),Image.LANCZOS)
def overlay(lines,size,y0,sub=None,label=None):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FT,size); fs=ImageFont.truetype(FS,42); fl=ImageFont.truetype(FS,34)
    lh=int(size*1.25); ys=[]
    y=y0
    if label: ys.append(('l',label,y)); y+=56
    for l in lines: ys.append(('t',l,y)); y+=lh
    yline=y+8; y+=36
    if sub: ys.append(('s',sub,y)); y+=56
    # sombra suave ceñida al texto
    m=Image.new('L',(W,H),0); dm=ImageDraw.Draw(m)
    for k,t,yy in ys:
        ff={'l':fl,'t':f,'s':fs}[k]; tw=dm.textlength(t,font=ff)
        dm.rounded_rectangle((90-30,yy-6,90+tw+30,yy+ff.size*1.3),radius=30,fill=55)
    m=m.filter(ImageFilter.GaussianBlur(34))
    sh=Image.new('RGBA',(W,H),(8,6,5,0)); sh.putalpha(m); im=Image.alpha_composite(sh,im); d=ImageDraw.Draw(im)
    for k,t,yy in ys:
        ff={'l':fl,'t':f,'s':fs}[k]; c={'l':GOLD,'t':WH,'s':WH}[k]
        d.text((91,yy+2),t,font=ff,fill=(0,0,0,170),stroke_width=2,stroke_fill=(0,0,0,110)); d.text((90,yy),t,font=ff,fill=c)
    d.line((90,yline,200,yline),fill=GOLD,width=4)
    d.text((90,1760),'@club.soberana',font=fl,fill=GOLD)
    return im
segs={
 'g': (D+'32-sofa-rojo-libro-sonriendo.jpg',0.5,['Hoy la cocina','está cerrada.'],90,250,None,None),
 'c1':(D+'29-comedor-taza-en-alto-sonriendo.jpg',0.45,['Café largo','y sin prisas.'],74,1130,None,'Plan de hoy'),
 'c3':(D+'31-sofa-rojo-leyendo-mirada.jpg',0.5,['¿Y tú, qué plan','tienes hoy?'],76,250,'Cuéntamelo abajo, te leo.',None),
}
for k,(p,cx,lines,sz,y0,sub,lab) in segs.items():
    b=fit(p,cx).convert('RGBA'); o=overlay(lines,sz,y0,sub,lab)
    Image.alpha_composite(b,o).convert('RGB').save(f'{k}.jpg',quality=95)
overlay(['Un libro, una peli…','y mi sofá rojo.'],74,260,None,'Plan de hoy').save('ov2.png')
