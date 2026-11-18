"""Música original (sintetizada, sin derechos) estilo pop cálido con ritmo, como la que le gusta a Coni (18 nov 2026).
Batería suave (bombo, palmada, charles), bajo, acordes de piano eléctrico, colchón de cuerdas y una melodía tipo «pluck».
Cada semilla cambia tonalidad, progresión, tempo (86-104 bpm) y melodía: la música va cambiando en cada publicación.
Uso: python3 scripts_musica_pop.py SALIDA.wav DURACION_S SEMILLA
"""
import sys, wave
import numpy as np

SR = 44100
PROGS = [  # grados (semitonos sobre la tónica menor relativa / mayor), tipo
    [(0, 'm'), (8, 'M'), (3, 'M'), (10, 'M')],    # i VI III VII
    [(0, 'm'), (8, 'M'), (10, 'M'), (7, 'M')],    # i VI VII V
    [(0, 'M'), (7, 'M'), (9, 'm'), (5, 'M')],     # I V vi IV
    [(0, 'M'), (9, 'm'), (5, 'M'), (7, 'M')],     # I vi IV V
    [(5, 'M'), (7, 'M'), (4, 'm'), (9, 'm')],     # IV V iii vi
    [(0, 'm'), (5, 'm'), (8, 'M'), (7, 'M')],     # i iv VI V
]
TRIADA = {'M': [0, 4, 7], 'm': [0, 3, 7]}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a=0.005, r=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)


def add(buf, sig, i):
    i = int(i)
    if i >= len(buf):
        return
    sig = sig[:len(buf) - i]
    buf[i:i + len(sig)] += sig


def kick(rng):
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.9


def clap(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    no = rng.normal(0, 1, n)
    no = np.convolve(no, np.ones(6) / 6, 'same') - np.convolve(no, np.ones(40) / 40, 'same')
    no = np.convolve(no, np.ones(4) / 4, 'same')
    return no * np.exp(-t * 18) * 0.28


def hat(rng, abierto=False):
    n = int((0.12 if abierto else 0.05) * SR); t = np.arange(n) / SR
    no = rng.normal(0, 1, n); no = no - np.convolve(no, np.ones(8) / 8, 'same')
    return no * np.exp(-t * (25 if abierto else 70)) * 0.045


def epiano(m, dur, vel):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t + 0.8 * np.exp(-t * 3) * np.sin(2 * np.pi * f * 2 * t))
    s += 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 2)
    return s * env(n, 0.004, 1.1) * vel


def pad(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = sum(np.sin(2 * np.pi * f * (1 + d) * t + p) for d, p in [(0, 0), (0.004, 1), (-0.004, 2)]) / 3
    a = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return s * a * 0.07


def bajo(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return s * env(n, 0.01, 0.6) * np.minimum(1, (dur - t) / 0.03).clip(0) * 0.32


def pluck(m, dur, vel):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t)
    s = np.convolve(s, np.ones(12) / 12, 'same')
    return s * env(n, 0.003, 0.25) * vel


def reverb(x, rng, seg=1.8, mezcla=0.22):
    n = int(seg * SR); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2); ir[0] = 0
    ir = np.convolve(ir, np.ones(30) / 30, 'same'); ir /= np.abs(ir).sum() / 6
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + n) * np.fft.rfft(ir, len(x) + n))[:len(x)]
    return x * (1 - mezcla) + wet * mezcla


def generar(dur, semilla):
    rng = np.random.default_rng(semilla)
    tonica = 57 + int(rng.integers(-3, 4))           # alrededor de La
    prog = PROGS[semilla % len(PROGS)]
    bpm = float(rng.integers(86, 105)); beat = 60 / bpm; bar = 4 * beat
    total = int((dur + 2) * SR)
    dr = np.zeros(total); ha = np.zeros(total); ba = np.zeros(total); ch = np.zeros(total); me = np.zeros(total)
    nb = int(np.ceil(dur / bar)) + 1
    escala = [0, 2, 3, 5, 7, 8, 10] if prog[0][1] == 'm' else [0, 2, 4, 5, 7, 9, 11]
    motivo = rng.choice(len(escala), 8)
    for b in range(nb):
        t0 = b * bar
        grado, tipo = prog[b % len(prog)]
        raiz = tonica + grado
        intro = b == 0
        for k in range(4):                           # batería
            tt = t0 + k * beat
            if not intro and k in (0, 2):
                add(dr, kick(rng), tt * SR)
            if k in (1, 3):
                add(dr, clap(rng), tt * SR)
            for h in (0, 0.5):
                add(ha, hat(rng, abierto=(h == 0.5 and k == 3)), (tt + h * beat) * SR)
        if not intro:                                # bajo: raíz con un pequeño empuje
            for k, (off, d) in enumerate([(0, 1.5), (1.5, 0.5), (2, 1.5), (3.5, 0.5)]):
                nota = raiz - 24 + (7 if k == 3 else 0)
                add(ba, bajo(nota, d * beat * 0.95), (t0 + off * beat) * SR)
        voces = [raiz + i for i in TRIADA[tipo]] + [raiz + 12]
        for off in (0, 1.5, 2.5):                    # piano eléctrico sincopado
            for v in voces:
                add(ch, epiano(v, beat * 1.4, 0.07), (t0 + off * beat) * SR)
        for v in voces[:3]:
            add(ch, pad(v - 12, bar), t0 * SR)
        if b >= 1:                                   # melodía pluck en corcheas
            for k in range(8):
                if rng.random() < 0.72:
                    g = (motivo[k] + (b % 2)) % len(escala)
                    nota = tonica + 12 + escala[g]
                    add(me, pluck(nota, beat * 0.5, 0.11), (t0 + k * beat / 2) * SR)
    mix = dr * 0.9 + ha + ba + reverb(ch, rng) + reverb(me, rng, mezcla=0.3)
    mix = mix[:int(dur * SR)]
    F = np.fft.rfft(mix); fq = np.fft.rfftfreq(len(mix), 1 / SR)
    mix = np.fft.irfft(F / np.sqrt(1 + (fq / 4500) ** 4), len(mix))   # paso bajo suave
    t = np.arange(len(mix)) / SR
    mix *= np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 1.5)
    mix = np.tanh(mix * 1.6) / np.tanh(1.6)
    mix /= np.abs(mix).max() / 0.85
    st = np.stack([mix, np.roll(mix, 120) * 0.97], 1)
    return st, f'{int(bpm)} bpm, tónica {tonica}, progresión {semilla % len(PROGS)}'


def escribir_wav(path, st):
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == '__main__':
    st, info = generar(float(sys.argv[2]), int(sys.argv[3]))
    escribir_wav(sys.argv[1], st)
    print(info)
