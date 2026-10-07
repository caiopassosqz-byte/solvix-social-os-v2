"""Trilha de um Reels do motor: usa a faixa do catálogo (tom, modo, acordes, timbres) e a
estrutura do vídeo (cenas, energia e efeitos sonoros exportados por motor.html).

    python3 reels/trilha.py D04 meta.json saida.wav

meta.json vem de render.js (DURATION, bpm, EVENTS, ESTRUTURA). Cada Reels mantém a
identidade harmônica da sua faixa no catálogo; o andamento segue o roteiro.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "trilhas"))
import arranjo  # noqa: E402
import gerador  # noqa: E402

G = ["pad", "arpejo", "bumbo", "baixo", "chimbal"]


def compassos(estrutura):
    out = []
    n = len(estrutura)
    for i, cena in enumerate(estrutura):
        nb = int(round(cena["compassos"]))
        e = cena["energia"]
        for k in range(nb):
            if e == "intro":
                cs = ["pad", "arpejo", "bumbo", "chimbal", "filtro"]
            elif e == "respiro":
                cs = ["pad", "arpejo"]
            elif e == "final":
                cs = G + ["caixa", "melodia"] + (["impacto"] if k == 0 else [])
            else:
                cs = G + ["caixa"]
                if k % 2 == 1 or nb == 1:
                    cs += ["aberto", "melodia"]
                if i == 1 and k == 0:
                    cs.append("impacto")
            ultimo = k == nb - 1
            if ultimo and i + 1 < n and estrutura[i + 1]["energia"] == "final":
                cs = [c for c in cs if c != "melodia"] + ["subida"]
            if ultimo and i + 1 < n and estrutura[i + 1].get("claro"):
                cs.append("subida")
            out.append(cs)
    return out


def ficha(rid, meta):
    cat = {f["id"]: f for f in json.load(open(os.path.join(AQUI, "..", "trilhas", "catalogo.json"), encoding="utf-8"))}
    f = cat[rid]
    return {
        "bpm": meta["bpm"], "tom": f["tom"], "modo": f["modo"], "progressao": f["progressao"], "nonas": f.get("nonas", False),
        "timbre_arpejo": f.get("timbre_arpejo", "pluck"), "arpejo": f.get("arpejo", 0), "passo": 0.25,
        "bumbo": gerador.BUMBOS.get(f.get("bumbo"), [0, 1, 2, 3]) if f.get("bumbo") != "meio-tempo" else [0, 1, 2, 3],
        "chimbal": gerador.CHIMBAIS.get(f.get("chimbal"), [0.5, 1.5, 2.5, 3.5]),
        "caixa": gerador.CAIXAS.get(f.get("caixa"), [1, 3]) if f.get("caixa") != "meio-tempo" else [1, 3],
        "brilho": max(3000, f.get("brilho", 2400) + 1000), "loudness": -14.5, "semente": f.get("semente", 7), "fade": 0.8,
        "g_pad": 1.7, "g_arp": 0.6 if f.get("timbre_arpejo") == "piano" else 0.55,
        "compassos": compassos(meta["estrutura"]),
        "efeitos": [[t, s] for t, s in meta["events"]],
    }


if __name__ == "__main__":
    rid, meta_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    meta = json.load(open(meta_path, encoding="utf-8"))
    d = arranjo.render(ficha(rid, meta), out, duracao=meta["dur"])
    print(rid, "trilha", round(d, 2), "s")
