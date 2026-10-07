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


def ficha(f):
    """Converte uma faixa do catálogo na ficha do arranjo (motor novo)."""
    v = f["variacao"]
    compassos = []
    efeitos = []
    beat = 60 / f["bpm"]
    bar = 4 * beat
    c = 0
    for nome, ncomp, cams in f["secoes"]:
        for k in range(ncomp):
            cs = [x for x in cams if x not in ("tique", "respiro", "subida")]
            if "subida" in cams and k == ncomp - 1:
                cs.append("subida")
            if "tique" in cams:
                for bt in range(4):
                    efeitos.append(["tique", (c + k) * bar + bt * beat])
            if "respiro" in cams and k == ncomp - 1:
                efeitos.append(["whoosh", (c + k + 1) * bar - 0.28])
            if nome == "intro" and v != "base" and "bumbo" not in cs:
                cs.append("filtro")
            compassos.append(cs)
        c += ncomp
    return {
        "bpm": f["bpm"], "tom": f["tom"], "modo": f["modo"], "progressao": f["progressao"], "nonas": f.get("nonas", False),
        "timbre_arpejo": "piano" if v == "base" else f.get("timbre_arpejo", "pluck"),
        "arpejo": f.get("arpejo", 0), "passo": 0.25 if v == "construcao" else 0.5,
        "bumbo": BUMBOS[f.get("bumbo", "reto")], "chimbal": CHIMBAIS[f.get("chimbal", "contratempo")], "caixa": CAIXAS[f.get("caixa", "palmas")],
        "brilho": f.get("brilho", 2400) + 900, "loudness": VARIACOES[v]["loudness"] + 1, "semente": f.get("semente", 7),
        "g_pad": 1.9 if v == "base" else 1.7, "g_arp": 0.75 if v == "base" else 0.55,
        "compassos": compassos, "efeitos": efeitos,
    }


def gerar(f):
    import arranjo
    nome = f["id"].lower()
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(DEMOS, exist_ok=True)
    wav = os.path.join(SAIDA, nome + ".wav")
    dur = arranjo.render(ficha(f), wav)
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
