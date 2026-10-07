#!/usr/bin/env python3
"""Prepara os Stories do ciclo: junta o plano, as peças prontas e os bastidores reais em stories/dados.js.

    python3 stories/preparar.py
    node stories/exportar.js            # gera stories/dNN/*.png

Por dia: 1 bastidor real da produção (almoço) e 1 story do post com uma pergunta (logo depois do post).
Segunda, quarta e sexta: 1 lembrete de palavra-chave. Os bastidores usam material de verdade:
o roteiro em código de cada Reels, a forma de onda da trilha, quadros do vídeo e a grade de slides.
"""
import datetime
import json
import os
import subprocess
import sys
import wave

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(R, "painel"))
sys.path.insert(0, os.path.join(R, "trilhas"))
import gerador  # noqa: E402
import montar  # noqa: E402

ASSETS = os.path.join(AQUI, "assets")
SEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def sh(*a):
    subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def duracao(mp4):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]).strip())


def quadros(pid, mp4):
    out = []
    d = duracao(mp4)
    from PIL import Image
    for k, f in enumerate((0.3, 0.52, 0.74)):
        dst = os.path.join(ASSETS, f"{pid.lower()}-q{k + 1}.jpg")
        for passo in range(12):  # evita quadros de transição (escuros ou vazios)
            t = d * f + passo * 0.4
            sh("ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=360:-1", "-q:v", "3", dst)
            im = Image.open(dst).convert("L")
            if np.asarray(im).std() > 30:
                break
        out.append("assets/" + os.path.basename(dst))
    return out, d


def onda(arquivo, n=72):
    tmp = os.path.join(ASSETS, "_onda.wav")
    sh("ffmpeg", "-y", "-i", arquivo, "-ac", "1", "-ar", "8000", tmp)
    with wave.open(tmp) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    os.remove(tmp)
    blocos = np.array_split(np.abs(x), n)
    v = np.array([np.sqrt(np.mean(b ** 2)) for b in blocos])
    return [round(float(a), 3) for a in (v / (v.max() or 1))]


def codigo(pid):
    arq = os.path.join(R, "reels", "roteiros", pid.lower() + ".js")
    if not os.path.exists(arq):
        return None
    js = (f"global.window={{}};require({json.dumps(arq)});const c=window.SPEC.cenas.slice(0,2);"
          "console.log(JSON.stringify(c,null,2))")
    txt = subprocess.check_output(["node", "-e", js], text=True)
    linhas = []
    for ln in txt.splitlines():
        ln = ln.replace('"tipo"', "tipo").replace('"compassos"', "compassos")
        for chave in ("linhas", "tamanho", "label", "site", "carregar", "destaques", "beat", "alvo", "texto", "sub", "rolar", "y", "dur",
                      "veredito", "titulo", "claro", "eyebrow", "itens", "passo", "top", "contador", "de", "ate", "inicio", "decisoes",
                      "antes", "depois", "revela", "degraus", "nome", "desc", "min", "max", "entrada", "toque", "mensagem", "digitar",
                      "riscar", "resultados", "linha", "tag", "resultadosBeat", "numero", "pares", "decTamanho", "depoisTamanho", "chip"):
            ln = ln.replace(f'"{chave}":', f"{chave}:")
        linhas.append(ln[:46] + ("…" if len(ln) > 46 else ""))
    return {"arquivo": f"reels/roteiros/{pid.lower()}.js", "linhas": linhas[:24]}


def main():
    os.makedirs(ASSETS, exist_ok=True)
    plano = json.load(open(os.path.join(AQUI, "roteiro.json"), encoding="utf-8"))["dias"]
    dados = montar.dados()
    cat = {f["id"]: f for f in json.load(open(os.path.join(R, "trilhas", "catalogo.json"), encoding="utf-8"))}
    inicio = datetime.date.fromisoformat(dados["inicio"])
    manifestos = [p["slides"][0] for p in dados["posts"] if p["fmt"] == "Imagem" and p.get("slides")]
    tipos_reels = ["codigo", "trilha", "quadros"]
    k_reels = 0
    dias = []
    for p in dados["posts"]:
        pid = p["id"]
        dia = inicio + datetime.timedelta(days=p["n"] - 1)
        roteiro = plano[pid]
        capa = p["slides"][0] if p.get("slides") else None
        item = {"id": pid, "n": p["n"], "data": f"{SEM[dia.weekday()]} {dia.day:02d}/{dia.month:02d}", "fmt": p["fmt"], "hook": p["hook"],
                "capa": capa and "../" + capa, "pergunta": roteiro["pergunta"], "resposta": roteiro["resposta"], "palavra": roteiro.get("palavra")}
        # bastidor da tarde
        b = None
        if p["fmt"] == "Reels" and p.get("video"):
            mp4 = os.path.join(R, p["video"])
            tipo = tipos_reels[k_reels % 3]
            k_reels += 1
            if tipo == "codigo" and not codigo(pid):
                tipo = "quadros"
            if tipo == "codigo":
                b = {"tipo": "codigo", "titulo": "O Reels de hoje começou [como código.]",
                     "texto": "Cada cena, palavra e movimento é escrito num roteiro. O vídeo é gerado a partir dele, quadro a quadro.", **codigo(pid)}
            elif tipo == "trilha":
                f = dict(cat[pid])
                f.setdefault("nonas", True)
                acordes = "Lám9 – Fá7M – Dó7M – Sol6" if pid == "D01" else " – ".join(gerador.nome_acorde(f, g) for g in f["progressao"])
                fonte = os.path.join(R, "posts/d01-teste-5-segundos/trilha-d01-v2.wav") if pid == "D01" else os.path.join(R, f"trilhas/demos/{pid.lower()}.mp3")
                b = {"tipo": "trilha", "titulo": "A música de hoje [foi feita para este vídeo.]", "onda": onda(fonte),
                     "texto": f"{gerador.NOTAS[f['tom']]} {f['modo']}, {f['bpm']} BPM, {acordes}. Cada efeito sonoro cai no tempo exato de um movimento."}
            else:
                qs, d = quadros(pid, mp4)
                b = {"tipo": "quadros", "titulo": "Três quadros [do Reels de hoje.]", "imgs": qs,
                     "texto": f"{round(d * 30)} quadros, 30 por segundo, cada movimento na batida da música."}
        elif p["fmt"] == "Carrossel" and p.get("slides"):
            b = {"tipo": "slides", "titulo": "O carrossel inteiro, [antes de ir ao ar.]", "imgs": ["../" + s for s in p["slides"]],
                 "texto": f"{len(p['slides'])} slides, revisados um a um no tamanho da tela do celular."}
        elif p["fmt"] == "Imagem":
            b = {"tipo": "slides", "titulo": "A linha editorial [do mês.]", "imgs": ["../" + s for s in manifestos],
                 "texto": "Três frases, o mesmo grid e a mesma tipografia. Uma por semana no feed."}
        else:
            b = {"tipo": "painel", "titulo": "Onde cada post [é planejado.]", "img": "assets/painel.png",
                 "texto": "Calendário, aprovação e resultado de cada post da Solvix num painel só."}
        item["bastidor"] = b
        dias.append(item)
    with open(os.path.join(AQUI, "dados.js"), "w", encoding="utf-8") as fh:
        fh.write("// Gerado por stories/preparar.py. Não edite à mão: edite stories/roteiro.json.\nwindow.DIAS = " + json.dumps(dias, ensure_ascii=False, indent=1) + ";\n")
    print(len(dias), "dias,", sum(1 for d in dias if d["palavra"]), "lembretes de palavra-chave")


if __name__ == "__main__":
    main()
