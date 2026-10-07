"""Trilha original do Reels D01 (Solvix): eletrônico minimalista, 112,5 BPM, 12 compassos (25,6 s).

Gera as faixas separadas em WAV e mixa com ffmpeg:
    python3 trilha.py            -> trilha-d01.wav

Mapa (1 compasso = 2,1333 s), alinhado aos cortes do vídeo:
    c0-1   hook         pad + arpejo + pulso leve
    c2-4   critérios    + bumbo e baixo
    c5-7   teste        + chimbal e palmas; subida de ruído no c7
    c8     veredito     impacto no tempo 1
    c9     "Agora abra o seu."  respiro: só pad e arpejo
    c10-11 CTA          groove de volta, saída em fade
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
BPM = 112.5
BEAT = 60 / BPM
BAR = 4 * BEAT
BARS = 12
DUR = BARS * BAR
N = int(DUR * SR) + SR  # 1 s de folga para caudas
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trilha-d01.wav")
rng = np.random.default_rng(7)

# Am9 - Fmaj7 - Cmaj7 - G6 (um acorde por compasso)
CHORDS = [
    (45, [57, 60, 64, 67, 71]),
    (41, [53, 57, 60, 64]),
    (48, [55, 60, 64, 71]),
    (43, [55, 59, 62, 64]),
]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_of(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def place(buf, sig, start):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += sig[: j - i]


def tri(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * np.abs(2 * ((f * t + phase) % 1) - 1) - 1


# ---- Pad (estéreo, levemente desafinado) ----
pad = np.zeros((N, 2))
for bar in range(BARS):
    if bar >= 11:
        continue
    _, notes = CHORDS[bar % 4]
    length = BAR + 0.6
    n = int(length * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / 0.45) * np.clip((length - t) / 0.6, 0, 1)
    for m in notes:
        for ch, cents in ((0, -6), (1, 6)):
            f = hz(m) * 2 ** (cents / 1200)
            place(pad[:, ch], 0.12 * env * tri(f, n, rng.random()), t_of(bar))
# último compasso: acorde final sustentado que some
_, notes = CHORDS[0]
n = int((BAR + 1.0) * SR)
t = np.arange(n) / SR
env = np.minimum(1, t / 0.45) * np.exp(-t / 1.2)
for m in notes:
    for ch, cents in ((0, -6), (1, 6)):
        place(pad[:, ch], 0.12 * env * tri(hz(m) * 2 ** (cents / 1200), n), t_of(11))

# ---- Arpejo (pluck) em colcheias ----
pluck = np.zeros(N)
for bar in range(BARS):
    _, notes = CHORDS[bar % 4]
    seq = [notes[k % len(notes)] + 12 for k in (0, 2, 1, 3, 2, 4, 1, 3)]
    for k, m in enumerate(seq):
        n = int(0.5 * SR)
        t = np.arange(n) / SR
        f = hz(m)
        sig = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t))
        vel = 0.9 if k % 2 == 0 else 0.6
        place(pluck, 0.22 * vel * sig * np.exp(-t / 0.13) * np.minimum(1, t / 0.004), t_of(bar, k * 0.5))

# ---- Bumbo ----
def kick_sig(gain=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 85 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return gain * 0.6 * np.sin(ph) * np.exp(-t / 0.16)

kick = np.zeros(N)
kick_times = []
for bar in list(range(2, 9)) + [10, 11]:
    for b in range(4):
        tk = t_of(bar, b)
        g = 0.8 if bar in (10, 11) else 1.0
        if bar == 11 and b > 1:
            continue
        place(kick, kick_sig(g), tk)
        kick_times.append(tk)
# pulso suave no hook
for b in range(8):
    if b in (0, 4):
        place(kick, kick_sig(0.45), b * BEAT)

# ---- Chimbal (contratempo) e palmas ----
hats = np.zeros(N)
claps = np.zeros(N)
for bar in list(range(5, 9)) + [10]:
    for b in range(4):
        n = int(0.06 * SR)
        t = np.arange(n) / SR
        place(hats, 0.18 * rng.standard_normal(n) * np.exp(-t / 0.018), t_of(bar, b + 0.5))
        if b in (1, 3):
            n2 = int(0.22 * SR)
            t2 = np.arange(n2) / SR
            env = np.exp(-t2 / 0.07) * (1 + 0.6 * np.exp(-((t2 - 0.012) / 0.004) ** 2))
            place(claps, 0.22 * rng.standard_normal(n2) * env, t_of(bar, b))
# ticks discretos no hook (marcam o cronômetro de 5 barras)
for b in range(2, 7):
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    place(hats, 0.10 * rng.standard_normal(n) * np.exp(-t / 0.01), b * BEAT)

# ---- Baixo (colcheias no contratempo) ----
bass = np.zeros(N)
for bar in list(range(2, 9)) + [10]:
    root, _ = CHORDS[bar % 4]
    for b in range(4):
        n = int(0.26 * SR)
        t = np.arange(n) / SR
        f = hz(root)
        sig = np.tanh(1.6 * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)))
        place(bass, 0.32 * sig * np.exp(-t / 0.18) * np.minimum(1, t / 0.01), t_of(bar, b + 0.5))

# ---- Efeitos: subida no c7, impacto no c8, respiro no c9 ----
fx = np.zeros(N)
n = int(BAR * SR)
t = np.arange(n) / SR
noise = rng.standard_normal(n)
noise = noise - np.concatenate(([0], noise[:-1]))  # mais agudo
place(fx, 0.12 * (t / BAR) ** 2.2 * noise, t_of(7))
n = int(1.6 * SR)
t = np.arange(n) / SR
boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.5)
tail = rng.standard_normal(n) * np.exp(-t / 0.35) * 0.25
place(fx, 0.7 * boom + 0.15 * tail, t_of(8))
n = int(BAR * 0.5 * SR)
t = np.arange(n) / SR
swell = rng.standard_normal(n) * (t / t[-1]) ** 3
place(fx, 0.08 * swell, t_of(9, 2))

# ---- Sidechain: pad e baixo abaixam a cada bumbo ----
duck = np.ones(N)
tt = np.arange(N) / SR
for tk in kick_times:
    i = int(tk * SR)
    j = min(N, i + int(0.35 * SR))
    duck[i:j] = np.minimum(duck[i:j], 1 - 0.55 * np.exp(-(tt[i:j] - tk) / 0.11))
pad *= duck[:, None]
bass *= duck


def write(path, data):
    data = np.atleast_2d(data.T).T if data.ndim == 1 else data
    pcm = np.clip(data, -1, 1)
    pcm = (pcm * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


with tempfile.TemporaryDirectory() as tmp:
    stems = {"pad": pad, "pluck": pluck, "kick": kick, "hats": hats, "claps": claps, "bass": bass, "fx": fx}
    for name, sig in stems.items():
        write(os.path.join(tmp, name + ".wav"), sig)
    inputs = []
    for name in stems:
        inputs += ["-i", os.path.join(tmp, name + ".wav")]
    graph = (
        "[0]lowpass=f=1900,aecho=0.8:0.5:120|260:0.25|0.18[pad];"
        "[1]lowpass=f=4200,aecho=0.8:0.7:400|800:0.32|0.16,pan=stereo|c0=0.8*c0|c1=0.55*c0[pl];"
        "[2]lowpass=f=900,pan=stereo|c0=c0|c1=c0[k];"
        "[3]highpass=f=6500,pan=stereo|c0=0.6*c0|c1=0.9*c0[h];"
        "[4]bandpass=f=1600:width_type=o:w=1.2,aecho=0.8:0.4:60:0.3,pan=stereo|c0=c0|c1=c0[c];"
        "[5]lowpass=f=420,pan=stereo|c0=c0|c1=c0[b];"
        "[6]highpass=f=30,pan=stereo|c0=c0|c1=c0[fx];"
        "[pad][pl][k][h][c][b][fx]amix=inputs=7:normalize=0,"
        f"atrim=0:{DUR:.3f},afade=t=out:st={DUR - 2.4:.3f}:d=2.4,"
        "loudnorm=I=-16:TP=-1.5:LRA=9,aresample=44100"
    )
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-ac", "2", OUT], check=True)
print("ok", OUT, f"{DUR:.2f}s")
