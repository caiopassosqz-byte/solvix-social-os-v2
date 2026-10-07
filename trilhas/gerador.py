#!/usr/bin/env python3
"""Gerador de trilhas originais para os Reels da Solvix.

Cada Reels recebe uma música própria: tom, modo, andamento, sequência de acordes,
arpejo, timbres e batida mudam de uma faixa para outra. O que se mantém é o
padrão de qualidade e o clima sóbrio da marca.

Uso:
    python3 trilhas/gerador.py catalogo            # cria catalogo.json (não sobrescreve)
    python3 trilhas/gerador.py catalogo --forcar   # recria o catálogo do zero
    python3 trilhas/gerador.py gerar D04           # gera trilhas/saida/d04.wav e trilhas/demos/d04.mp3
    python3 trilhas/gerador.py gerar todos

Para sincronizar com um vídeo pronto, edite "secoes" da faixa no catalogo.json:
uma lista de [nome, compassos, [camadas]]. Camadas disponíveis:
pad, arpejo, melodia, tique, bumbo, bumbo_leve, baixo, chimbal, caixa,
subida (ruído que sobe no último compasso), impacto (no 1º tempo),
respiro (ruído curto no fim da seção).
"""
import json
import os
import subprocess
import sys
import tempfile
import wave
import zlib

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(AQUI, "catalogo.json")
SAIDA = os.path.join(AQUI, "saida")
DEMOS = os.path.join(AQUI, "demos")
SR = 44100

NOTAS = ["Dó", "Dó#", "Ré", "Mi♭", "Mi", "Fá", "Fá#", "Sol", "Lá♭", "Lá", "Si♭", "Si"]
MODOS = {
    "menor": [0, 2, 3, 5, 7, 8, 10],
    "dórico": [0, 2, 3, 5, 7, 9, 10],
    "maior": [0, 2, 4, 5, 7, 9, 11],
    "lídio": [0, 2, 4, 6, 7, 9, 11],
    "mixolídio": [0, 2, 4, 5, 7, 9, 10],
}
# Graus da escala (0 = tônica), um acorde por compasso
PROGRESSOES = {
    "menor": [[0, 5, 2, 6], [0, 3, 5, 4], [5, 3, 0, 6], [0, 6, 5, 6], [0, 2, 5, 3], [3, 4, 0, 0], [0, 5, 3, 4]],
    "dórico": [[0, 3, 0, 6], [0, 1, 3, 0], [0, 6, 3, 4], [0, 2, 3, 6]],
    "maior": [[0, 4, 5, 3], [0, 5, 3, 4], [3, 4, 2, 5], [0, 2, 3, 4], [5, 3, 0, 4]],
    "lídio": [[0, 1, 0, 4], [0, 1, 5, 4], [5, 1, 0, 0]],
    "mixolídio": [[0, 6, 3, 0], [0, 4, 6, 3], [6, 3, 0, 0]],
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
BUMBOS = {"reto": [0, 1, 2, 3], "quebrado": [0, 1.5, 2.5], "meio-tempo": [0, 2.5], "sincopado": [0, 0.75, 2, 2.75]}
CHIMBAIS = {"contratempo": [0.5, 1.5, 2.5, 3.5], "semicolcheias": [i * 0.25 for i in range(16)], "shaker": [i * 0.5 for i in range(8)]}
CAIXAS = {"palmas": [1, 3], "aro": [1.75, 3], "meio-tempo": [2]}

VARIACOES = {
    "pulso": {
        "descricao": "Eletrônico minimalista; as camadas entram uma a uma",
        "bpm": (104, 116), "modos": ["menor", "dórico", "maior"], "loudness": -16,
        "pads": ["triangulo", "serra-suave", "seno-tremolo"], "arpejos": ["pluck", "sino"],
        "bumbos": ["reto", "quebrado", "sincopado"], "chimbais": ["contratempo", "shaker", "semicolcheias"],
        "caixas": ["palmas", "aro"],
        "secoes": [["intro", 2, ["pad", "arpejo", "tique", "bumbo_leve"]],
                   ["entrada", 3, ["pad", "arpejo", "bumbo", "baixo"]],
                   ["pico", 3, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "caixa", "melodia", "subida"]],
                   ["impacto", 1, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "caixa", "melodia", "impacto"]],
                   ["respiro", 1, ["pad", "arpejo", "respiro"]],
                   ["final", 2, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "melodia"]]],
    },
    "construcao": {
        "descricao": "Batida mais marcada, para timelapse de projeto",
        "bpm": (116, 124), "modos": ["menor", "mixolídio", "dórico"], "loudness": -16,
        "pads": ["serra-suave", "triangulo"], "arpejos": ["pluck", "sino"],
        "bumbos": ["reto", "sincopado"], "chimbais": ["semicolcheias", "contratempo"],
        "caixas": ["palmas", "aro"],
        "secoes": [["intro", 1, ["pad", "arpejo", "tique"]],
                   ["groove", 4, ["pad", "arpejo", "bumbo", "baixo", "chimbal"]],
                   ["pico", 4, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "caixa", "melodia", "subida"]],
                   ["impacto", 1, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "caixa", "impacto"]],
                   ["respiro", 1, ["pad", "arpejo", "respiro"]],
                   ["final", 3, ["pad", "arpejo", "bumbo", "baixo", "chimbal", "melodia"]]],
    },
    "base": {
        "descricao": "Teclado e arpejo sem bateria, para ficar por baixo da voz",
        "bpm": (76, 90), "modos": ["maior", "lídio", "menor"], "loudness": -18,
        "pads": ["seno-tremolo", "triangulo"], "arpejos": ["piano"],
        "bumbos": ["meio-tempo"], "chimbais": ["shaker"], "caixas": ["meio-tempo"],
        "secoes": [["intro", 2, ["pad"]],
                   ["corpo", 6, ["pad", "arpejo"]],
                   ["meio", 4, ["pad", "arpejo", "melodia"]],
                   ["final", 4, ["pad", "arpejo"]]],
    },
}

REELS = [
    ("D01", "pulso", "Abra seu site no celular. Você tem 5 segundos."),
    ("D03", "base", "A Solvix não nasceu para fazer site bonito."),
    ("D04", "construcao", "Mesma empresa. Mesmo serviço. Só mudamos a primeira tela."),
    ("D06", "pulso", "Seu site é bonito. Mas ele vende?"),
    ("D08", "pulso", "Seu cliente não pesquisa seu nome. Ele pesquisa o que você faz."),
    ("D10", "base", "Um site pode custar R$1 mil ou R$35 mil. Aqui está a diferença."),
    ("D11", "pulso", "O botão mais importante do seu site está escondido."),
    ("D12", "construcao", "Por que esse site imobiliário quase não usa cor."),
    ("D13", "base", "Comecei o Instagram da Solvix com 0 seguidores. Vou mostrar tudo."),
    ("D14", "construcao", "Redesenhei a página de uma academia em 3 decisões."),
    ("D16", "pulso", "Fiz o teste dos 5 segundos em 3 sites. Só um passou."),
    ("D19", "pulso", "Seu perfil no Google é a primeira página do seu site."),
    ("D20", "construcao", "O site traz o contato. O que acontece depois?"),
    ("D21", "pulso", "\"Qualidade e excelência\" não diz nada."),
    ("D23", "construcao", "Numa loja online, a venda acontece ou morre na página do produto."),
    ("D24", "base", "Seu site não passou no teste dos 5 segundos? Eu faço a análise."),
    ("D25", "base", "As perguntas que mais chegaram na DM da Solvix este mês."),
    ("D26", "pulso", "Seu site foi feito em 2019. Seu cliente percebe."),
    ("D28", "pulso", "O site de R$300 costuma custar duas vezes."),
    ("D30", "base", "30 dias atrás: 0 seguidores. Estes são os números de hoje."),
]


# ---------------------------------------------------------------- catálogo

def criar_catalogo(forcar=False):
    if os.path.exists(CATALOGO) and not forcar:
        print("catalogo.json já existe (use --forcar para recriar)")
        return
    usados = {(9, "menor", (0, 5, 2, 6))}  # combinação da trilha aprovada do D01
    faixas = []
    anterior = None
    for rid, var, hook in REELS:
        if rid == "D01":
            faixas.append({"id": rid, "hook": hook, "variacao": var, "status": "aprovada",
                           "arquivo": "posts/d01-teste-5-segundos/trilha-d01.wav",
                           "tom": 9, "modo": "menor", "bpm": 112.5, "progressao": [0, 5, 2, 6]})
            anterior = faixas[-1]
            continue
        v = VARIACOES[var]
        rng = np.random.default_rng(zlib.crc32(rid.encode()))
        for _ in range(500):
            modo = str(rng.choice(v["modos"]))
            tom = int(rng.integers(0, 12))
            prog = PROGRESSOES[modo][int(rng.integers(len(PROGRESSOES[modo])))]
            if (tom, modo, tuple(prog)) in usados:
                continue
            if anterior and (tom == anterior["tom"] or prog == anterior["progressao"]):
                continue
            break
        usados.add((tom, modo, tuple(prog)))
        f = {
            "id": rid, "hook": hook, "variacao": var, "status": "rascunho",
            "tom": tom, "modo": modo, "progressao": prog,
            "bpm": int(rng.integers(v["bpm"][0], v["bpm"][1] + 1)),
            "arpejo": int(rng.integers(len(ARPEJOS))),
            "timbre_arpejo": str(rng.choice(v["arpejos"])),
            "pad": str(rng.choice(v["pads"])),
            "bumbo": str(rng.choice(v["bumbos"])),
            "chimbal": str(rng.choice(v["chimbais"])),
            "caixa": str(rng.choice(v["caixas"])),
            "nonas": bool(rng.random() < 0.5),
            "eco": float(rng.choice([0.5, 0.75, 1.0])),
            "brilho": int(rng.integers(1500, 2700)),
            "semente": int(rng.integers(1, 10_000)),
            "secoes": v["secoes"],
        }
        faixas.append(f)
        anterior = f
    with open(CATALOGO, "w", encoding="utf-8") as fh:
        json.dump(faixas, fh, ensure_ascii=False, indent=1)
    print(f"catálogo com {len(faixas)} faixas em {CATALOGO}")


# ---------------------------------------------------------------- síntese

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


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
    escala = MODOS[f["modo"]]
    graus = [grau, grau + 2, grau + 4, grau + 6] + ([grau + 8] if f["nonas"] else [])
    return [nota_grau(f["tom"], escala, g) for g in graus]


def nome_acorde(f, grau):
    notas = acorde(f, grau)
    r = notas[0] % 12
    terca = (notas[1] - notas[0]) % 12
    quinta = (notas[2] - notas[0]) % 12
    setima = (notas[3] - notas[0]) % 12
    q = "m" if terca == 3 else ""
    if quinta == 6:
        q = "m7(♭5)"
    elif setima == 11:
        q += "7M"
    else:
        q += "7"
    return NOTAS[r] + q


def onda(tipo, freq, n, fase=0.0):
    t = np.arange(n) / SR
    if tipo == "triangulo":
        return 2 * np.abs(2 * ((freq * t + fase) % 1) - 1) - 1
    if tipo == "serra-suave":
        s = np.zeros(n)
        for k in range(1, 9):
            s += np.sin(2 * np.pi * k * freq * t + fase * k) / k ** 1.3
        return 0.6 * s
    trem = 1 + 0.25 * np.sin(2 * np.pi * 4.2 * t + fase)
    return (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)) * trem * 0.8


def nota_tocada(tipo, m, dur, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    if tipo == "sino":
        s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.1) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.05)
        env = np.exp(-t / 0.35)
    elif tipo == "piano":
        s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.4) + 0.25 * np.sin(6 * np.pi * f * t) * np.exp(-t / 0.2) + 0.1 * np.sin(8 * np.pi * f * t) * np.exp(-t / 0.1)
        env = np.exp(-t / 0.9)
    else:  # pluck
        s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
        env = np.exp(-t / 0.13)
    return vel * s * env * np.minimum(1, t / 0.004)


def coloca(buf, sig, inicio):
    i = int(inicio * SR)
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += sig[: j - i]


def bumbo_sig(ganho, grave):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    fr = grave + 85 * np.exp(-t / 0.035)
    return ganho * 0.6 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.16)


def sintetizar(f):
    rng = np.random.default_rng(f["semente"])
    beat = 60 / f["bpm"]
    bar = 4 * beat
    total = sum(s[1] for s in f["secoes"])
    dur = total * bar
    N = int(dur * SR) + 2 * SR
    camadas = {k: np.zeros(N) for k in ("arpejo", "melodia", "bumbo", "chimbal", "caixa", "baixo", "fx")}
    pad = np.zeros((N, 2))
    batidas = []
    prog = f["progressao"]
    escala = MODOS[f["modo"]]
    grave = 40 + rng.integers(0, 14)
    timbre = f.get("timbre_arpejo", "pluck")
    padrao = ARPEJOS[f.get("arpejo", 0)]
    passo = 0.25 if f["variacao"] == "construcao" else 0.5
    # motivo de melodia: 2 compassos, 5 notas, registro agudo
    pos = sorted(rng.choice(16, size=5, replace=False).tolist())
    motivo = [(p * 0.5, int(rng.integers(0, 4))) for p in pos]

    c = 0
    for nome, ncomp, cams in f["secoes"]:
        cams = set(cams)
        for k in range(ncomp):
            t0 = (c + k) * bar
            grau = prog[(c + k) % len(prog)]
            notas = [dobrar(n, 52, 76) for n in acorde(f, grau)]
            raiz = dobrar(nota_grau(f["tom"], escala, grau), 36, 48)
            ultimo = k == ncomp - 1
            if "pad" in cams:
                ln = bar + 0.6
                n = int(ln * SR)
                t = np.arange(n) / SR
                env = np.minimum(1, t / 0.45) * np.clip((ln - t) / 0.6, 0, 1)
                for m in notas:
                    for ch, cents in ((0, -6), (1, 6)):
                        coloca(pad[:, ch], 0.11 * env * onda(f["pad"], hz(m) * 2 ** (cents / 1200), n, rng.random()), t0)
            if "arpejo" in cams:
                tons = sorted(notas)
                passos = int(4 / passo)
                for s in range(passos):
                    idx = padrao[s % len(padrao)]
                    if idx is None:
                        continue
                    m = tons[idx % len(tons)] + 12 * (1 + idx // len(tons))
                    vel = 0.9 if s % 2 == 0 else 0.6
                    amp = 0.25 if timbre == "piano" else 0.2
                    coloca(camadas["arpejo"], amp * nota_tocada(timbre, m, 1.4 if timbre == "piano" else 0.6, vel), t0 + s * passo * beat)
            if "melodia" in cams:
                tons = sorted(dobrar(n, 72, 86) for n in notas)
                for (b, i) in motivo:
                    tb = b - 4 * ((c + k) % 2)
                    if 0 <= tb < 4:
                        coloca(camadas["melodia"], 0.09 * nota_tocada("sino", tons[i % len(tons)], 1.2), t0 + tb * beat)
            if "bumbo" in cams or "bumbo_leve" in cams:
                pat = BUMBOS[f["bumbo"]] if "bumbo" in cams else [0]
                g = 1.0 if "bumbo" in cams else 0.45
                for b in pat:
                    coloca(camadas["bumbo"], bumbo_sig(g, grave), t0 + b * beat)
                    if "bumbo" in cams:
                        batidas.append(t0 + b * beat)
            if "baixo" in cams:
                for b in range(4):
                    n = int(0.26 * SR)
                    t = np.arange(n) / SR
                    fr = hz(raiz)
                    s = np.tanh(1.6 * (np.sin(2 * np.pi * fr * t) + 0.25 * np.sin(4 * np.pi * fr * t)))
                    coloca(camadas["baixo"], 0.32 * s * np.exp(-t / 0.18) * np.minimum(1, t / 0.01), t0 + (b + 0.5) * beat)
            if "chimbal" in cams:
                for i, b in enumerate(CHIMBAIS[f["chimbal"]]):
                    longo = f["chimbal"] == "shaker"
                    n = int((0.09 if longo else 0.06) * SR)
                    t = np.arange(n) / SR
                    acento = 1.0 if (i % 2 == 1 or len(CHIMBAIS[f["chimbal"]]) <= 4) else 0.55
                    coloca(camadas["chimbal"], 0.18 * acento * rng.standard_normal(n) * np.exp(-t / (0.03 if longo else 0.018)), t0 + b * beat)
            if "tique" in cams:
                for b in range(4):
                    n = int(0.03 * SR)
                    t = np.arange(n) / SR
                    coloca(camadas["chimbal"], 0.1 * rng.standard_normal(n) * np.exp(-t / 0.01), t0 + b * beat)
            if "caixa" in cams:
                for b in CAIXAS[f["caixa"]]:
                    n = int(0.22 * SR)
                    t = np.arange(n) / SR
                    env = np.exp(-t / 0.07) * (1 + 0.6 * np.exp(-((t - 0.012) / 0.004) ** 2))
                    g = 0.16 if f["caixa"] == "aro" else 0.22
                    coloca(camadas["caixa"], g * rng.standard_normal(n) * env, t0 + b * beat)
            if "subida" in cams and ultimo:
                n = int(bar * SR)
                t = np.arange(n) / SR
                ru = rng.standard_normal(n)
                ru = ru - np.concatenate(([0], ru[:-1]))
                coloca(camadas["fx"], 0.12 * (t / bar) ** 2.2 * ru, t0)
            if "impacto" in cams and k == 0:
                n = int(1.6 * SR)
                t = np.arange(n) / SR
                boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.5)
                coloca(camadas["fx"], 0.7 * boom + 0.04 * rng.standard_normal(n) * np.exp(-t / 0.35), t0)
            if "respiro" in cams and ultimo:
                n = int(bar * 0.5 * SR)
                t = np.arange(n) / SR
                coloca(camadas["fx"], 0.08 * rng.standard_normal(n) * (t / t[-1]) ** 3, t0 + bar / 2)
        c += ncomp

    # sidechain: pad e baixo abaixam a cada bumbo
    duck = np.ones(N)
    tt = np.arange(N) / SR
    for tk in batidas:
        i = int(tk * SR)
        j = min(N, i + int(0.35 * SR))
        duck[i:j] = np.minimum(duck[i:j], 1 - 0.55 * np.exp(-(tt[i:j] - tk) / 0.11))
    pad *= duck[:, None]
    camadas["baixo"] *= duck
    return pad, camadas, dur, beat


def grava_wav(caminho, dados):
    if dados.ndim == 1:
        dados = dados[:, None]
    pcm = (np.clip(dados, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def gerar(f):
    pad, cam, dur, beat = sintetizar(f)
    eco = int(f["eco"] * beat * 1000)
    loud = VARIACOES[f["variacao"]]["loudness"]
    nome = f["id"].lower()
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(DEMOS, exist_ok=True)
    wav = os.path.join(SAIDA, nome + ".wav")
    with tempfile.TemporaryDirectory() as tmp:
        ordem = [("pad", pad)] + list(cam.items())
        entradas = []
        for k, sig in ordem:
            p = os.path.join(tmp, k + ".wav")
            grava_wav(p, sig)
            entradas += ["-i", p]
        g = (
            f"[0]lowpass=f={f['brilho']},aecho=0.8:0.5:120|260:0.25|0.18[pad];"
            f"[1]lowpass=f=4500,aecho=0.8:0.7:{eco}|{2 * eco}:0.32|0.16,pan=stereo|c0=0.8*c0|c1=0.55*c0[arp];"
            f"[2]highpass=f=500,aecho=0.8:0.8:{eco}:0.35,pan=stereo|c0=0.55*c0|c1=0.85*c0[mel];"
            "[3]lowpass=f=900,pan=stereo|c0=c0|c1=c0[bum];"
            "[4]highpass=f=6500,pan=stereo|c0=0.6*c0|c1=0.9*c0[chi];"
            "[5]bandpass=f=1600:width_type=o:w=1.2,aecho=0.8:0.4:60:0.3,pan=stereo|c0=c0|c1=c0[cai];"
            "[6]lowpass=f=420,pan=stereo|c0=c0|c1=c0[bai];"
            "[7]highpass=f=30,pan=stereo|c0=c0|c1=c0[fx];"
            "[pad][arp][mel][bum][chi][cai][bai][fx]amix=inputs=8:normalize=0,"
            f"atrim=0:{dur:.3f},afade=t=in:d=0.05,afade=t=out:st={dur - 2.4:.3f}:d=2.4,"
            f"loudnorm=I={loud}:TP=-1.5:LRA=9,aresample=44100"
        )
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", g, "-ac", "2", wav], check=True)
    mp3 = os.path.join(DEMOS, nome + ".mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", mp3], check=True)
    acordes = " – ".join(nome_acorde(f, g) for g in f["progressao"])
    print(f"{f['id']}  {f['variacao']:<10} {NOTAS[f['tom']]} {f['modo']:<9} {f['bpm']:>5} BPM  {dur:5.1f}s  {acordes}")
    return wav


def main(argv):
    if not argv or argv[0] not in ("catalogo", "gerar"):
        print(__doc__)
        return 1
    if argv[0] == "catalogo":
        criar_catalogo("--forcar" in argv)
        return 0
    with open(CATALOGO, encoding="utf-8") as fh:
        faixas = json.load(fh)
    alvo = [a.upper() for a in argv[1:]]
    for f in faixas:
        if f.get("status") == "aprovada":
            continue
        if "TODOS" in alvo or f["id"] in alvo:
            gerar(f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
