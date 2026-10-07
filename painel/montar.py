#!/usr/bin/env python3
"""Monta o painel do Solvix Social OS.

Junta o plano (painel/plano.json), as legendas das peças prontas, as trilhas
(trilhas/catalogo.json) e o modelo (painel/modelo.html) em um arquivo só.

    python3 painel/montar.py                 # gera index.html na raiz do repositório
    python3 painel/montar.py --artifact X    # também gera a versão para publicar como Artifact em X

As imagens e áudios são referenciados pelo caminho a partir da raiz do repositório
(posts/..., trilhas/demos/..., marca/...), então o index.html abre direto no navegador.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "trilhas"))
import gerador  # noqa: E402

INICIO = "2026-10-12"


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as fh:
        return fh.read()


def secao(md, titulo, ate="\n## "):
    i = md.index(titulo) + len(titulo)
    j = md.find(ate, i)
    return md[i: j if j >= 0 else None].strip()


def limpa(txt):
    txt = re.sub(r"\*\*Legenda\*\*\s*", "", txt)
    return txt.strip()


def legendas():
    out = {}
    out["D01"] = secao(ler("posts/d01-teste-5-segundos/roteiro.md"), "## Legenda")
    out["D02"] = secao(ler("posts/d02-anatomia-landing-page/legenda.md"), "## Legenda")
    out["D12"] = secao(ler("posts/kaza-projeto/legenda.md"), "## Legenda")
    m = ler("posts/manifestos/legendas.md")
    for d in ("D09", "D25", "D27"):
        bloco = m[m.index("## " + d):]
        bloco = bloco[bloco.index("**Legenda**"):]
        fim = bloco.find("\n## ", 1)
        out[d] = limpa(bloco[: fim if fim >= 0 else None])
    return out


PECAS = {
    "D01": {"slides": ["posts/d01-teste-5-segundos/capa.png"], "video": "posts/d01-teste-5-segundos/reels-d01-com-trilha.mp4",
            "pasta": "posts/d01-teste-5-segundos/"},
    "D02": {"slides": [f"posts/d02-anatomia-landing-page/slide-{i:02d}.png" for i in range(1, 10)], "pasta": "posts/d02-anatomia-landing-page/"},
    "D09": {"slides": ["posts/manifestos/manifesto-d09.png"], "pasta": "posts/manifestos/"},
    "D12": {"slides": [f"posts/kaza-projeto/slide-{i:02d}.png" for i in range(1, 7)], "pasta": "posts/kaza-projeto/"},
    "D25": {"slides": ["posts/manifestos/manifesto-d25.png"], "pasta": "posts/manifestos/"},
    "D27": {"slides": ["posts/manifestos/manifesto-d27.png"], "pasta": "posts/manifestos/"},
}

PENDENCIAS = [
    {"id": "publicacao", "titulo": "Conectar a publicação automática",
     "detalhe": "Crie uma conta no Postiz e conecte o Instagram da Solvix (conta profissional ligada a uma página do Facebook). Depois, adicione a chave da API nas configurações do ambiente do Claude com o nome POSTIZ_API_KEY. Não cole a chave no chat. Até lá, os posts aprovados ficam prontos para você subir manualmente."},
    {"id": "arroba", "titulo": "Confirmar o @ da agência", "detalhe": "Usei @solvixagency nas prévias e na bio sugerida."},
    {"id": "link", "titulo": "Enviar o link da bio", "detalhe": "Ele entra na bio e nos botões \"Ver projetos\"."},
    {"id": "horario", "titulo": "Definir o horário de publicação", "detalhe": "Escolha em Estratégia › Ajustes do ciclo. Vale para todos os posts até você mudar."},
    {"id": "kaza", "titulo": "Autorização do Grupo Kaza", "detalhe": "Para publicar o D12 com o nome e as fotos da Kaza.", "posts": [12]},
    {"id": "materiais", "titulo": "Materiais das palavras-chave", "detalhe": "Checklist de landing page, guia de investimento e roteiro da análise gratuita. Posso escrever os três; preciso do seu ok no conteúdo.", "posts": [5, 10, 17, 24]},
    {"id": "politicas", "titulo": "Confirmar as políticas da Solvix", "detalhe": "Domínio no nome do cliente, contrato, pagamento em etapas e entrega de acessos, citados no D17 e no D29.", "posts": [17, 29]},
]


def trilhas():
    cat = json.loads(ler("trilhas/catalogo.json"))
    out = {}
    for f in cat:
        if f["id"] == "D01":
            acordes = "Lám9 – Fá7M – Dó7M – Sol6"
        else:
            f.setdefault("nonas", True)
            acordes = " – ".join(gerador.nome_acorde(f, g) for g in f["progressao"])
        out[f["id"]] = {
            "arquivo": f"trilhas/demos/{f['id'].lower()}.mp3",
            "variacao": {"pulso": "Pulso", "construcao": "Construção", "base": "Base"}[f["variacao"]],
            "tom": gerador.NOTAS[f["tom"]] + " " + f["modo"],
            "bpm": f["bpm"],
            "acordes": acordes,
            "status": f["status"],
            "hook": f["hook"],
        }
    return out


def dados():
    plano = json.loads(ler("painel/plano.json"))
    leg = legendas()
    trs = trilhas()
    posts = []
    for i, p in enumerate(plano["posts"]):
        pid = f"D{i + 1:02d}"
        p = dict(p)
        p.pop("previa", None)
        p.pop("peca", None)
        p["id"] = pid
        p["n"] = i + 1
        if pid in PECAS:
            p.update(PECAS[pid])
        if pid in leg:
            p["legenda"] = leg[pid]
        if p["fmt"] == "Reels" and pid in trs:
            p["trilha"] = trs[pid]
        p["statusInicial"] = "revisao" if pid in PECAS else "planejado"
        posts.append(p)
    return {
        "inicio": INICIO,
        "funcs": plano["funcs"],
        "pilares": plano["pilares"],
        "hooks": plano["hooks"],
        "paleta": plano["paleta"],
        "posts": posts,
        "pendencias": PENDENCIAS,
        "trilhas": [dict(id=k, **v) for k, v in trs.items()],
    }


def main(argv):
    modelo = ler("painel/modelo.html")
    corpo = modelo.replace("/*__DADOS__*/null", json.dumps(dados(), ensure_ascii=False))
    doc = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
           "</head>\n<body>\n" + corpo + "\n</body>\n</html>\n")
    with open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("index.html atualizado")
    if "--artifact" in argv:
        destino = argv[argv.index("--artifact") + 1]
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(corpo)
        print("artifact em", destino)


if __name__ == "__main__":
    main(sys.argv[1:])
