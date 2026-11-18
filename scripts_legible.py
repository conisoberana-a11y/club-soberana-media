# Oscurece con suavidad solo el fondo detrás de las letras blancas de la frase (no toca las letras). Uso: legible.py ENTRADA SALIDA
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
im = Image.open(sys.argv[1]).convert('RGB'); a = np.asarray(im).astype(float)
b = (a.min(2) > 232) & (a.max(2) - a.min(2) < 22)
b[int(im.height * 0.5):] = False; b[:, :60] = False
ys, xs = np.nonzero(b)
if len(xs) > 400:
    x0, x1 = np.percentile(xs, 1), np.percentile(xs, 99); y0, y1 = np.percentile(ys, 1), np.percentile(ys, 99)
    reg = a[int(y0):int(y1), int(x0):int(x1)].mean(2)
    if reg[~b[int(y0):int(y1), int(x0):int(x1)]].mean() > 120:
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((x0 - 130, y0 - 80, x1 + 130, y1 + 80), fill=95)
        mm = np.asarray(m.filter(ImageFilter.GaussianBlur(60))).astype(float) / 255
        t = np.clip((a.min(2) - 205) / 40, 0, 1)
        w = np.clip((mm * (1 - t))[..., None] * 1.25, 0, 0.7)
        a = a * (1 - w) + np.array([28, 20, 14]) * w
Image.fromarray(a.clip(0, 255).astype('uint8')).save(sys.argv[2], quality=95)
