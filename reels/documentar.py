"""Escreve posts/<pasta>/roteiro.md de um Reels a partir do roteiro (reels/roteiros/dNN.js).

    python3 reels/documentar.py d03 d03-por-que-a-solvix-existe [legenda.txt]

Sem arquivo de legenda, mantém a seção "## Legenda" do roteiro.md que já existe na pasta.
"""
import json
import os
import subprocess
import sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "trilhas"))
import gerador  # noqa: E402

F = {"A": "Atração", "Au": "Autoridade", "R": "Relacionamento", "C": "Conversão"}


def limpa(s):
    return s.replace("[", "").replace("]", "")


def desc(c):
    t = c["tipo"]
    if t in ("palavras", "cta"):
        return " / ".join(limpa(x) for x in c["linhas"]) + (f" ({c['sub']})" if c.get("sub") else "")
    if t == "celular":
        bits = [d["texto"] for d in c.get("destaques", [])]
        if c.get("contador"):
            bits.insert(0, f"contador {c['contador']['de']}→{c['contador']['ate']}")
        if c.get("toque"):
            bits.append("toque no botão")
        if c.get("mensagem"):
            bits.append("mensagem chega: \"" + c["mensagem"]["texto"] + "\"")
        if c.get("veredito"):
            bits.append("**" + c["veredito"]["titulo"] + "** " + c["veredito"].get("sub", ""))
        return f"Celular com o site \"{c['site']}\"" + (f" ({c['label']})" if c.get("label") else "") + ": " + "; ".join(bits)
    if t == "antesdepois":
        return f"Antes e depois ({c['antes']} → {c['depois']}), revelado por uma linha: " + "; ".join(c.get("decisoes", []))
    if t == "lista":
        return c["eyebrow"] + ": " + " · ".join(limpa(x) for x in c["itens"])
    if t == "escada":
        return c["eyebrow"] + ": " + " · ".join(d["nome"] for d in c["degraus"]) + f" ({c['min']} – {c['max']})"
    if t == "busca":
        return "Busca: " + " → ".join(d["texto"] + (" (riscado)" if d.get("riscar") else "") for d in c["digitar"]) + "; **" + c["veredito"]["titulo"] + "**"
    if t == "numero":
        return f"{c.get('antes', '')} **{c['numero']}** {c.get('depois', '')}"
    if t == "reescrita":
        return c["eyebrow"] + ": " + " | ".join(p["antes"] + " → " + p["depois"] for p in c["pares"])
    return t


def main(rid, slug, legenda=None):
    ID = rid.upper()
    n = int(rid[1:])
    plano = json.load(open(os.path.join(R, "painel/plano.json"), encoding="utf-8"))["posts"][n - 1]
    spec = json.loads(subprocess.check_output(["node", "-e", f"global.window={{}};require('{R}/reels/roteiros/{rid}.js');console.log(JSON.stringify(window.SPEC))"]))
    pasta = os.path.join(R, "posts", slug)
    destino = os.path.join(pasta, "roteiro.md")
    if legenda:
        leg = open(legenda, encoding="utf-8").read().strip()
    else:
        md = open(destino, encoding="utf-8").read()
        leg = md[md.index("## Legenda") + len("## Legenda"):].strip()
    bar = 240 / spec["bpm"]
    t = 0
    rows = []
    for i, c in enumerate(spec["cenas"]):
        d = c["compassos"] * bar
        rows.append(f"| {t:4.1f} – {t + d:4.1f} s | {i + 1:02d} · {c['tipo']}{' (claro)' if c.get('claro') else ''} | {desc(c)} |")
        t += d
    cat = {f["id"]: f for f in json.load(open(os.path.join(R, "trilhas/catalogo.json"), encoding="utf-8"))}
    f = cat[ID]
    f.setdefault("nonas", True)
    acordes = " – ".join(gerador.nome_acorde(f, g) for g in f["progressao"])
    md = f"""# {ID} · {plano['tema']}

- **Função:** {F[plano['f']]} · **Métrica:** {plano['metrica']}
- **Formato:** Reels 1080×1920, {t:.1f} s, {spec['bpm']} BPM
  - `reels-{rid}.mp4`: com a trilha original e os efeitos sonoros
  - `reels-{rid}-mudo.mp4`: sem som, para usar um áudio da biblioteca do Instagram
- **Capa:** `capa.png` (o hook completo, dentro do corte 3:4 da grade)
- **Fonte editável:** `reels/roteiros/{rid}.js` (abra `reels/motor.html?r={rid}`; `render(t)` mostra o quadro do segundo t)
- **Trilha:** {gerador.NOTAS[f['tom']]} {f['modo']}, {acordes}, {spec['bpm']} BPM. Gerada por `reels/trilha.py` com os efeitos nos tempos exatos dos movimentos. Prévia em `trilhas/demos/{rid}.mp3`.

## Roteiro

| Tempo | Cena | Na tela |
|---|---|---|
""" + "\n".join(rows) + f"""

## Legenda

{leg}
"""
    os.makedirs(pasta, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(md)
    print("ok", destino)


if __name__ == "__main__":
    main(*sys.argv[1:])
