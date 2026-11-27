"""Monta la frase del día sobre las animaciones de Flow (animar/lentos/AAAA-MM-DD.mp4, ya a 16 s).
Uso: python3 animar/montar.py 2026-12-05 [2026-12-09 ...]  (desde fondos-frase/)
Texto: animar/textos.json. Posición (x,y): animar/posiciones.json (por defecto 90,300). Sonido: pajaritos de lentos/05_lavanda.m4a.
Salida: animar/final/frase-AAAA-MM-DD.mp4"""
import sys,json,subprocess
T=json.load(open('animar/textos.json')); P=json.load(open('animar/posiciones.json'))
for f in sys.argv[1:]:
    pos=P.get(f,[90,300]); x,y=pos[0],pos[1]; claro=pos[2] if len(pos)>2 else None
    a={'video':f'animar/lentos/{f}.mp4','audio':'lentos/05_lavanda.m4a','bloques':T[f]['bloques'],'x':x,'y':y,'claro':claro,'salida':f'animar/final/frase-{f}.mp4'}
    subprocess.run(['python3','frase_video.py',json.dumps(a)],check=True)
