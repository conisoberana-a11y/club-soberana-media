# Lleva una tarjeta 4:5 a 9:16 sin bandas: escala un poco (recorte lateral mínimo) y prolonga arriba y abajo
# con un reflejo suavizado de la propia imagen, fundido con degradado.
import sys
from PIL import Image, ImageFilter, ImageOps
W, H, S = 1080, 1920, 1.08
im = Image.open(sys.argv[1]).convert('RGB')
import numpy as np
from PIL import ImageDraw as _D
a = np.asarray(im).astype(int)
blanco = (a.min(2) > 232) & (a.max(2) - a.min(2) < 22)
blanco[int(im.height * 0.62):] = False          # el texto de la frase está arriba
blanco[:, :40] = False
ys, xs = np.nonzero(blanco)
if len(xs) > 400:
    x0, x1 = np.percentile(xs, 1), np.percentile(xs, 99); y0, y1 = np.percentile(ys, 1), np.percentile(ys, 99)
    fondo = a[int(y0):int(y1), int(x0):int(x1)].mean(2)
    if fondo[~blanco[int(y0):int(y1), int(x0):int(x1)]].mean() > 120:   # fondo claro: oscurecer suave
        m = Image.new('L', im.size, 0)
        _D.Draw(m).ellipse((x0 - 120, y0 - 70, x1 + 120, y1 + 70), fill=95)
        m = m.filter(ImageFilter.GaussianBlur(55))
        # oscurecer solo el fondo: cuanto más blanco es el píxel (letras), menos se oscurece
        mm = np.asarray(m).astype(float) / 255
        t = np.clip((a.min(2) - 205) / 40, 0, 1)
        wgt = (mm * (1 - t))[..., None] * 1.25
        res_ = a * (1 - np.clip(wgt, 0, 0.7)) + np.array([28, 20, 14]) * np.clip(wgt, 0, 0.7)
        im = Image.fromarray(res_.clip(0, 255).astype('uint8'))
w, h = int(im.width * S), int(im.height * S)
im = im.resize((w, h), Image.LANCZOS).crop(((w - W) // 2, 0, (w - W) // 2 + W, h))
g = (H - h) // 2
out = Image.new('RGB', (W, H))
out.paste(im, (0, g))
def tira(region, flip):
    t = ImageOps.flip(region) if flip else region
    t = t.filter(ImageFilter.GaussianBlur(18))
    return t
arriba = tira(im.crop((0, 0, W, g + 60)), True)
abajo = tira(im.crop((0, h - g - 60, W, h)), True)
out.paste(arriba.crop((0, 0, W, g + 60)), (0, 0))
out.paste(abajo, (0, g + h - 60))
# fundido en la costura
mask = Image.new('L', (W, H), 0)
from PIL import ImageDraw
d = ImageDraw.Draw(mask)
for y in range(120):
    a = int(255 * (1 - y / 120))
    d.line((0, g + y, W, g + y), fill=a)
    d.line((0, g + h - 1 - y, W, g + h - 1 - y), fill=a)
d.rectangle((0, 0, W, g), fill=255); d.rectangle((0, g + h, W, H), fill=255)
base = Image.new('RGB', (W, H)); base.paste(im, (0, g))
blur = out.filter(ImageFilter.GaussianBlur(10))
res = Image.composite(blur, base, mask)
res.save(sys.argv[2], quality=95)
