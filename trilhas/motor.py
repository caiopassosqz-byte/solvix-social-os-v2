"""Motor de som das trilhas Solvix.

Instrumentos sintetizados em numpy com mais corpo que a primeira versão:
supersaw para pads, pluck e piano com harmônicos que decaem em velocidades
diferentes, sinos inarmônicos, bateria com ataque e sub, reverberação por
convolução e efeitos sonoros para sincronizar com o vídeo (whoosh, tique,
impacto, clique, pop, chime, subida, glitch).
"""
import subprocess
import tempfile
import wave
import os

import numpy as np

SR = 44100
RNG = np.random.default_rng(11)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(n):
    return np.arange(n) / SR


def env_ar(n, a=0.005, r=None):
    t = t_(n)
    e = np.minimum(1, t / max(a, 1e-4))
    if r:
        e *= np.clip((n / SR - t) / r, 0, 1)
    return e


# ------------------------------------------------------------------ filtros

def fft_band(x, lo=None, hi=None, slope=0.25):
    """Passa-faixa suave no domínio da frequência (x mono ou estéreo)."""
    if x.ndim == 2:
        return np.stack([fft_band(x[:, c], lo, hi, slope) for c in range(x.shape[1])], axis=1)
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / (1 + (f / hi) ** (2 / slope * 0.5))
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 / slope * 0.5))
    return np.fft.irfft(X * g, n)


def sweep(x, f0, f1, width=0.6, frame=1024):
    """Filtro de banda que varre de f0 a f1 ao longo do sinal (whoosh, subida)."""
    n = len(x)
    hop = frame // 2
    win = np.hanning(frame)
    out = np.zeros(n + frame)
    f = np.fft.rfftfreq(frame, 1 / SR)
    pos = 0
    while pos < n:
        seg = np.zeros(frame)
        chunk = x[pos:pos + frame]
        seg[:len(chunk)] = chunk
        k = pos / max(1, n - 1)
        fc = f0 * (f1 / f0) ** k
        mask = np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / width) ** 2)
        out[pos:pos + frame] += np.fft.irfft(np.fft.rfft(seg * win) * mask, frame)
        pos += hop
    return out[:n]


def reverb_ir(dur=2.2, decay=0.55, seed=3):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    t = t_(n)
    env = np.exp(-t / decay) * (1 - np.exp(-t / 0.012))
    ir = rng.standard_normal((n, 2)) * env[:, None]
    ir = fft_band(ir, hi=6500)
    for d, g in ((0.011, 0.6), (0.019, 0.45), (0.027, 0.35)):
        i = int(d * SR)
        ir[i, 0] += g
        ir[i + 37, 1] += g
    return ir / np.sqrt((ir ** 2).sum(axis=0, keepdims=True))


_IR = None


def reverb(x, wet=0.25):
    """Convolução estéreo (x estéreo)."""
    global _IR
    if _IR is None:
        _IR = reverb_ir()
    n = len(x) + len(_IR) - 1
    N = 1 << (n - 1).bit_length()
    out = np.zeros((len(x), 2))
    for c in range(2):
        y = np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(_IR[:, c], N), N)[:len(x)]
        out[:, c] = y
    return x * (1 - wet) + out * wet * 0.9


def pan(x, p=0.0):
    """p de -1 (esquerda) a 1 (direita); x mono -> estéreo."""
    l = np.cos((p + 1) * np.pi / 4)
    r = np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], axis=1) * 1.41


# ------------------------------------------------------------------ instrumentos

def supersaw(m, dur, voices=3, cents=11, fmax=2400):
    n = int(dur * SR)
    t = t_(n)
    out = np.zeros((n, 2))
    f0 = hz(m)
    for v in range(voices):
        det = (v - (voices - 1) / 2) * cents / max(1, voices - 1) * 2
        f = f0 * 2 ** (det / 1200)
        ph = RNG.random() * 2 * np.pi
        s = np.zeros(n)
        k = 1
        while k * f < fmax:
            s += np.sin(2 * np.pi * k * f * t + ph * k) / k
            k += 1
        p = -0.6 + 1.2 * v / max(1, voices - 1)
        out += pan(s * 0.5 / voices, p)
    return out


def pluck(m, dur=0.7, vel=1.0, bright=1.0):
    n = int(dur * SR)
    t = t_(n)
    f = hz(m)
    s = np.zeros(n)
    for k in range(1, 13):
        if k * f > 9000:
            break
        tau = 0.22 * bright / (1 + 0.55 * (k - 1))
        s += np.sin(2 * np.pi * k * f * t) * np.exp(-t / tau) / k ** 1.1
    s2 = np.sin(2 * np.pi * f * 1.004 * t) * np.exp(-t / 0.18) * 0.35
    return vel * (s + s2) * np.minimum(1, t / 0.003) * 0.5


def piano(m, dur=1.6, vel=1.0):
    n = int(dur * SR)
    t = t_(n)
    f = hz(m)
    B = 0.0004
    s = np.zeros(n)
    for k in range(1, 11):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 10000:
            break
        s += np.sin(2 * np.pi * fk * t) * np.exp(-t / (1.6 / (1 + 0.35 * k))) / k ** 1.3
    ham = RNG.standard_normal(n) * np.exp(-t / 0.004) * 0.08
    return vel * (s + ham) * np.minimum(1, t / 0.002) * 0.55


def bell(m, dur=1.6, vel=1.0):
    n = int(dur * SR)
    t = t_(n)
    f = hz(m)
    s = np.zeros(n)
    for r, a, d in ((1, 1, 1.2), (2.0, 0.4, 0.8), (2.76, 0.35, 0.5), (4.07, 0.2, 0.3), (5.4, 0.12, 0.2)):
        s += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d)
    return vel * s * np.minimum(1, t / 0.002) * 0.45


def kick(gain=1.0, tone=48):
    n = int(0.55 * SR)
    t = t_(n)
    fr = tone + 110 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.2)
    click = RNG.standard_normal(n) * np.exp(-t / 0.0025)
    click = np.diff(click, prepend=0) * 0.35
    knock = np.sin(2 * np.pi * 130 * t) * np.exp(-t / 0.03) * 0.45
    return gain * np.tanh(1.4 * (body * 0.8 + knock + click)) * 0.55


def clap(gain=1.0):
    n = int(0.35 * SR)
    t = t_(n)
    e = np.zeros(n)
    for d in (0.0, 0.011, 0.022):
        e += np.exp(-np.maximum(t - d, 0) / 0.006) * (t >= d)
    e += np.exp(-np.maximum(t - 0.03, 0) / 0.09) * (t >= 0.03) * 0.6
    s = fft_band(RNG.standard_normal(n), lo=900, hi=5000)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.04) * 0.3
    return gain * (s * e + tone) * 0.5


def hat(gain=1.0, open_=False):
    n = int((0.3 if open_ else 0.07) * SR)
    t = t_(n)
    s = np.zeros(n)
    for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0):
        s += np.sign(np.sin(2 * np.pi * f * 8.0 * t + RNG.random() * 6))
    s = s / 6 + RNG.standard_normal(n) * 0.5
    s = np.diff(np.diff(s, prepend=0), prepend=0)
    return gain * s * np.exp(-t / (0.09 if open_ else 0.018)) * 0.22


def bass(m, dur=0.3, gain=1.0):
    n = int(dur * SR)
    t = t_(n)
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    return gain * np.tanh(2.4 * s) * np.exp(-t / (dur * 0.7)) * np.minimum(1, t / 0.008) * 0.34


# ------------------------------------------------------------------ efeitos

def sfx_whoosh(dur=0.45, up=True, gain=1.0):
    n = int(dur * SR)
    t = t_(n)
    x = RNG.standard_normal(n)
    x = sweep(x, 300 if up else 6000, 6000 if up else 300, width=0.7)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return gain * x * env * 0.9


def sfx_tick(gain=1.0, f=1900):
    n = int(0.05 * SR)
    t = t_(n)
    return gain * (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + RNG.standard_normal(n) * np.exp(-t / 0.003) * 0.3) * 0.5


def sfx_pop(gain=1.0):
    n = int(0.12 * SR)
    t = t_(n)
    fr = 90 + 140 * np.exp(-t / 0.02)
    return gain * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.05) * 0.7


def sfx_impact(gain=1.0):
    n = int(1.8 * SR)
    t = t_(n)
    boom = np.sin(2 * np.pi * (34 + 60 * np.exp(-t / 0.06)) * t) * np.exp(-t / 0.55)
    nz = fft_band(RNG.standard_normal(n), hi=2500) * np.exp(-t / 0.25) * 0.5
    return gain * np.tanh(1.3 * (boom + nz)) * 0.8


def sfx_click(gain=1.0):
    n = int(0.03 * SR)
    t = t_(n)
    return gain * (np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006) + RNG.standard_normal(n) * np.exp(-t / 0.002) * 0.5) * 0.6


def sfx_chime(m=88, gain=1.0):
    a = bell(m, 1.4, 0.8)
    b = bell(m + 7, 1.4, 0.8)
    out = np.zeros(int(1.6 * SR))
    out[:len(a)] += a
    i = int(0.11 * SR)
    out[i:i + len(b)] += b[:len(out) - i]
    return gain * out * 0.6


def sfx_riser(dur=1.8, gain=1.0):
    n = int(dur * SR)
    t = t_(n)
    x = sweep(RNG.standard_normal(n), 400, 9000, width=0.9)
    tone = np.sin(2 * np.pi * np.cumsum(200 * 6 ** (t / dur)) / SR) * 0.15
    return gain * (x * 0.8 + tone) * (t / dur) ** 2


def sfx_glitch(dur=0.35, gain=1.0):
    n = int(dur * SR)
    out = np.zeros(n)
    pos = 0
    while pos < n:
        ln = int(RNG.uniform(0.012, 0.03) * SR)
        if RNG.random() < 0.6:
            seg = fft_band(RNG.standard_normal(ln), lo=600, hi=7000) if ln > 64 else RNG.standard_normal(ln)
            out[pos:pos + ln] += seg[:n - pos] * 0.5
        pos += ln + int(0.01 * SR)
    return gain * out


# ------------------------------------------------------------------ utilidades

def place(buf, sig, start):
    i = int(round(start * SR))
    if i < 0:
        sig = sig[-i:]
        i = 0
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += sig[: j - i]


def duck(n, hits, depth=0.55, rel=0.11):
    g = np.ones(n)
    tt = t_(n)
    for tk in hits:
        i = int(tk * SR)
        j = min(n, i + int(0.4 * SR))
        if i < n:
            g[i:j] = np.minimum(g[i:j], 1 - depth * np.exp(-(tt[i:j] - tk) / rel))
    return g


def write_wav(path, x):
    if x.ndim == 1:
        x = x[:, None]
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def master(x, path, dur, loud=-15, fade_in=0.02, fade_out=1.6):
    """Cola, limita e normaliza o volume com ffmpeg."""
    x = x[: int(dur * SR)]
    x = np.tanh(x * 1.1) / np.tanh(1.1)
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "mix.wav")
        write_wav(raw, x * 0.8)
        af = (f"highpass=f=40,equalizer=f=2800:t=q:w=1.2:g=3,treble=g=2.5:f=6000,acompressor=threshold=0.25:ratio=2.5:attack=8:release=120:makeup=1.4,"
              f"afade=t=in:d={fade_in},afade=t=out:st={max(0, dur - fade_out):.3f}:d={fade_out},"
              f"loudnorm=I={loud}:TP=-1.2:LRA=8,aresample=44100")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ac", "2", path], check=True)
