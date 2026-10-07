"""Arranjo: transforma uma ficha de faixa (tom, acordes, compassos, camadas e efeitos) em áudio.

Ficha mínima:
    {
      "bpm": 120, "tom": 9, "modo": "menor", "progressao": [0, 5, 2, 6], "nonas": True,
      "compassos": [["pad", "arpejo", "bumbo"], ...],      # uma lista de camadas por compasso
      "efeitos": [["whoosh", 1.82], ["tique", 4.5], ...],  # [tipo, segundo]
      "timbre_arpejo": "pluck" | "piano" | "sino", "padrao_arpejo": [...], "passo": 0.5,
      "bumbo": [0, 1, 2, 3], "chimbal": [0.5, 1.5, 2.5, 3.5], "caixa": [1, 3],
      "brilho": 2200, "loudness": -15, "semente": 7
    }
Camadas por compasso: pad, arpejo, melodia, bumbo, bumbo_leve, baixo, chimbal, caixa,
aberto (chimbal aberto no contratempo), subida (no compasso inteiro), impacto (tempo 1),
corte (silencia a bateria na segunda metade), filtro (abafa o compasso, para intro).
"""
import numpy as np

import motor as M

MODOS = {
    "menor": [0, 2, 3, 5, 7, 8, 10],
    "dórico": [0, 2, 3, 5, 7, 9, 10],
    "maior": [0, 2, 4, 5, 7, 9, 11],
    "lídio": [0, 2, 4, 6, 7, 9, 11],
    "mixolídio": [0, 2, 4, 5, 7, 9, 10],
}
ARPEJOS = [
    [0, 2, 1, 3, 2, 4, 1, 3],
    [0, 1, 2, 3, 4, 3, 2, 1],
    [0, None, 2, None, 1, 3, None, 2],
    [3, 2, 1, 0, 3, 2, 1, 0],
    [0, 4, 2, 5, 1, 4, 3, 5],
    [0, 2, 4, 2, 1, 3, 5, 3],
    [None, 0, 2, 1, None, 3, 2, 4],
]


def nota_grau(tom, escala, grau, base=48):
    oit, i = divmod(grau, 7)
    return base + tom + 12 * oit + escala[i]


def dobrar(n, lo, hi):
    while n < lo:
        n += 12
    while n >= hi:
        n -= 12
    return n


def acorde(f, grau):
    esc = MODOS[f["modo"]]
    graus = [grau, grau + 2, grau + 4, grau + 6] + ([grau + 8] if f.get("nonas") else [])
    return [nota_grau(f["tom"], esc, g) for g in graus]


SFX = {
    "whoosh": lambda: M.sfx_whoosh(0.45, True, 0.55),
    "whoosh_desce": lambda: M.sfx_whoosh(0.45, False, 0.5),
    "tique": lambda: M.sfx_tick(0.55),
    "tique_agudo": lambda: M.sfx_tick(0.6, 2600),
    "pop": lambda: M.sfx_pop(0.6),
    "impacto": lambda: M.sfx_impact(0.9),
    "clique": lambda: M.sfx_click(0.7),
    "chime": lambda: M.sfx_chime(88, 0.7),
    "glitch": lambda: M.sfx_glitch(0.35, 0.45),
}


def render(f, saida, duracao=None):
    rng = np.random.default_rng(f.get("semente", 7))
    beat = 60 / f["bpm"]
    bar = 4 * beat
    nb = len(f["compassos"])
    dur = duracao or nb * bar
    N = int((nb * bar + 3) * M.SR)
    pad = np.zeros((N, 2))
    arp = np.zeros(N)
    mel = np.zeros(N)
    kick = np.zeros(N)
    hats = np.zeros(N)
    snr = np.zeros(N)
    bas = np.zeros(N)
    fx = np.zeros(N)
    filt_bars = []
    hits = []
    esc = MODOS[f["modo"]]
    prog = f["progressao"]
    padrao = f.get("padrao_arpejo") or ARPEJOS[f.get("arpejo", 0)]
    passo = f.get("passo", 0.5)
    timbre = f.get("timbre_arpejo", "pluck")
    pos = sorted(rng.choice(16, size=5, replace=False).tolist())
    motivo = [(p * 0.5, int(rng.integers(0, 4))) for p in pos]
    kpat = f.get("bumbo", [0, 1, 2, 3])
    hpat = f.get("chimbal", [0.5, 1.5, 2.5, 3.5])
    spat = f.get("caixa", [1, 3])
    tone = f.get("grave", 52)

    for b, cams in enumerate(f["compassos"]):
        cams = set(cams)
        t0 = b * bar
        grau = prog[b % len(prog)]
        notas = [dobrar(n, 52, 76) for n in acorde(f, grau)]
        raiz = dobrar(nota_grau(f["tom"], esc, grau), 40, 52)
        corte = "corte" in cams
        if "filtro" in cams:
            filt_bars.append(b)
        if "pad" in cams:
            ln = bar + 0.5
            env = np.minimum(1, M.t_(int(ln * M.SR)) / 0.25) * np.clip((ln - M.t_(int(ln * M.SR))) / 0.5, 0, 1)
            for m in notas:
                s = M.supersaw(m, ln)
                M.place(pad[:, 0], s[:, 0] * env * 0.16, t0)
                M.place(pad[:, 1], s[:, 1] * env * 0.16, t0)
        if "arpejo" in cams:
            tons = sorted(notas)
            for k in range(int(4 / passo)):
                idx = padrao[k % len(padrao)]
                if idx is None:
                    continue
                m = tons[idx % len(tons)] + 12 * (1 + idx // len(tons))
                vel = (0.95 if k % 2 == 0 else 0.62) * rng.uniform(0.9, 1.05)
                fn = {"piano": M.piano, "sino": M.bell}.get(timbre, M.pluck)
                M.place(arp, (fn(m, 0.7, vel, 1.4) if fn is M.pluck else fn(m, 1.4, vel)) * (0.95 if timbre == "piano" else 1.05), t0 + k * passo * beat)
        if "melodia" in cams:
            tons = sorted(dobrar(n, 74, 88) for n in notas)
            for (bt, i) in motivo:
                tb = bt - 4 * (b % 2)
                if 0 <= tb < 4:
                    M.place(mel, M.bell(tons[i % len(tons)], 1.4, 0.55), t0 + tb * beat)
        if "bumbo" in cams or "bumbo_leve" in cams:
            pat = kpat if "bumbo" in cams else [0]
            g = 1.0 if "bumbo" in cams else 0.55
            for bt in pat:
                if corte and bt >= 2:
                    continue
                M.place(kick, M.kick(g, tone), t0 + bt * beat)
                hits.append(t0 + bt * beat)
        if "baixo" in cams:
            for bt in range(4):
                if corte and bt >= 2:
                    continue
                M.place(bas, M.bass(raiz, 0.32, 1.0), t0 + (bt + 0.5) * beat)
        if "chimbal" in cams:
            for i, bt in enumerate(hpat):
                if corte and bt >= 2:
                    continue
                g = (1.0 if (bt * 2) % 2 == 1 else 0.6) * rng.uniform(0.85, 1.05)
                jit = rng.normal(0, 0.003)
                M.place(hats, M.hat(g), t0 + bt * beat + jit)
        if "aberto" in cams:
            for bt in (0.5, 1.5, 2.5, 3.5):
                if corte and bt >= 2:
                    continue
                M.place(hats, M.hat(0.55, True), t0 + bt * beat)
        if "caixa" in cams:
            for bt in spat:
                if corte and bt >= 2:
                    continue
                M.place(snr, M.clap(0.9), t0 + bt * beat)
        if "subida" in cams:
            M.place(fx, M.sfx_riser(bar, 0.5), t0)
        if "impacto" in cams:
            M.place(fx, M.sfx_impact(0.8), t0)

    for tipo, seg in f.get("efeitos", []):
        M.place(fx, SFX[tipo](), seg)

    # sidechain e filtro de intro
    g = M.duck(N, hits)
    pad *= g[:, None]
    bas *= g
    for b in filt_bars:
        i, j = int(b * bar * M.SR), int((b + 1) * bar * M.SR)
        for arr in (arp, kick, hats, snr, bas):
            seg = arr[i:j].copy()
            arr[i:j] = M.fft_band(seg, hi=900) if len(seg) > 0 else seg
        pad[i:j] = M.fft_band(pad[i:j], hi=900)

    brilho = f.get("brilho", 3200)
    pad = M.fft_band(pad, hi=brilho)
    musical = pad * f.get("g_pad", 1.7) + M.pan(arp, -0.25) * f.get("g_arp", 0.55) + M.pan(mel, 0.3) * 0.8
    musical = M.reverb(musical, 0.32)
    perc = M.pan(kick, 0) * 0.85 + M.pan(M.fft_band(hats, lo=4500), 0.2) * 3.2 + M.reverb(M.pan(snr, 0), 0.18) + M.pan(M.fft_band(bas, lo=60, hi=900), 0)
    efeitos = M.reverb(M.pan(fx, 0), 0.22)
    mix = musical * 0.9 + perc + efeitos * 0.9
    M.master(mix, saida, dur, loud=f.get("loudness", -15), fade_out=f.get("fade", 1.6))
    return dur
