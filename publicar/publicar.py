#!/usr/bin/env python3
"""Publica no Instagram (@solvixagencybr) os posts e Stories do ciclo, na hora da agenda, pela API da Meta.

    python3 publicar/publicar.py jpg                         # gera as versões JPEG (a API só aceita JPEG em imagem)
    python3 publicar/publicar.py agenda [--dia D01]          # lista o que sai e quando
    python3 publicar/publicar.py testar D01-post             # cria o contêiner na Meta e para antes de publicar
    python3 publicar/publicar.py devidos --aprovados D01,D02 [--seco] [--agora 2026-10-08T19:00]

`devidos` publica o que está na hora (do horário marcado até JANELA minutos depois), só dos posts
aprovados no painel, e anota cada publicação em publicar/registro.json. Nada sai duas vezes: antes de
publicar um post, confere o registro e as últimas publicações do perfil.

O token fica no segredo META_TOKEN do ambiente, injetado nas chamadas a graph.facebook.com.
As mídias são lidas pela Meta direto do repositório público (raw.githubusercontent.com).
"""
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(R, "painel"))
import montar  # noqa: E402

GRAPH = "https://graph.facebook.com/v21.0"
IG = "17841417373153450"  # @solvixagencybr
RAW = "https://raw.githubusercontent.com/caiopassosqz-byte/solvix-social-os-v2/claude/clever-darwin-t5nvmp/"
FUSO = datetime.timezone(datetime.timedelta(hours=-3))  # horário de Brasília
JANELA = 60  # minutos de tolerância depois do horário marcado (menor que o intervalo entre dois Stories seguidos)
REGISTRO = os.path.join(AQUI, "registro.json")
STORIES = {"01-bastidor.png": "bastidor", "02-post.png": "story_post", "03-palavra.png": "palavra"}


def jpg_de(png):
    return "publicar/jpg/" + png[:-4] + ".jpg"


def itens():
    d = montar.dados()
    inicio = datetime.date.fromisoformat(d["inicio"])
    out = []
    for p in d["posts"]:
        dia = inicio + datetime.timedelta(days=p["n"] - 1)
        ag = d["agenda"]["fds" if dia.weekday() >= 5 or dia.isoformat() in d["agenda"].get("feriados", {}) else "util"]  # feriado segue o fim de semana

        def quando(chave):
            h, m = map(int, ag[chave].split(":"))
            return datetime.datetime(dia.year, dia.month, dia.day, h, m, tzinfo=FUSO)

        if p["fmt"] == "Reels" and p.get("video"):
            post = {"tipo": "reels", "video": p["video"], "capa": (p.get("slides") or [None])[0]}
        elif p["fmt"] == "Carrossel" and len(p.get("slides") or []) > 1:
            post = {"tipo": "carrossel", "imagens": p["slides"][:10]}
        elif p.get("slides"):
            post = {"tipo": "imagem", "imagens": p["slides"][:1]}
        else:
            post = None  # peça ainda não produzida (D13, D30)
        if post:
            out.append(dict(post, chave=f"{p['id']}-post", post=p["id"], quando=quando("post"), legenda=p.get("legenda", "")))
        for st in p.get("stories", []):
            nome = os.path.basename(st["arquivo"])
            out.append({"chave": f"{p['id']}-{nome[:2]}", "post": p["id"], "tipo": "story", "imagens": [st["arquivo"]],
                        "quando": quando(STORIES[nome])})
    return sorted(out, key=lambda i: i["quando"])


# ---------- API ----------

def api(caminho, dados=None, metodo=None):
    url = GRAPH + caminho
    corpo = urllib.parse.urlencode(dados).encode() if dados is not None else None
    req = urllib.request.Request(url, data=corpo, method=metodo or ("POST" if corpo else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{caminho}: {e.read().decode()[:400]}") from None


def esperar(cid, limite=600):
    t0 = time.time()
    while True:
        st = api(f"/{cid}?fields=status_code,status")
        if st.get("status_code") == "FINISHED":
            return
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"contêiner {cid}: {st.get('status')}")
        if time.time() - t0 > limite:
            raise RuntimeError(f"contêiner {cid} não ficou pronto em {limite}s")
        time.sleep(8)


def conteiner(it):
    url = lambda rel: RAW + urllib.parse.quote(rel)  # noqa: E731
    if it["tipo"] == "reels":
        d = {"media_type": "REELS", "video_url": url(it["video"]), "caption": it["legenda"], "share_to_feed": "true"}
        if it.get("capa"):
            d["cover_url"] = url(jpg_de(it["capa"]))
        cid = api(f"/{IG}/media", d)["id"]
    elif it["tipo"] == "carrossel":
        filhos = [api(f"/{IG}/media", {"image_url": url(jpg_de(s)), "is_carousel_item": "true"})["id"] for s in it["imagens"]]
        for f in filhos:
            esperar(f)
        cid = api(f"/{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": it["legenda"]})["id"]
    elif it["tipo"] == "imagem":
        cid = api(f"/{IG}/media", {"image_url": url(jpg_de(it["imagens"][0])), "caption": it["legenda"]})["id"]
    else:
        cid = api(f"/{IG}/media", {"media_type": "STORIES", "image_url": url(jpg_de(it["imagens"][0]))})["id"]
    esperar(cid)
    return cid


def ja_no_perfil(it):
    """Confere no próprio Instagram se o item já saiu, caso o registro não tenha sido salvo.

    Story: algum Story ativo publicado entre 5 minutos antes do horário marcado e o fim da janela
    (dois Stories da agenda nunca ficam a menos de 90 minutos um do outro). Post: legenda igual
    entre as últimas publicações do feed."""
    if it["tipo"] == "story":
        ini = it["quando"] - datetime.timedelta(minutes=5)
        fim = it["quando"] + datetime.timedelta(minutes=JANELA + 30)
        for s in api(f"/{IG}/stories?fields=id,timestamp,permalink").get("data", []):
            ts = datetime.datetime.strptime(s["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            if ini <= ts <= fim:
                return s
        return None
    if not it.get("legenda"):
        return None
    ini = it["legenda"].strip()[:80]
    for m in api(f"/{IG}/media?fields=id,caption,permalink&limit=15").get("data", []):
        if (m.get("caption") or "").strip()[:80] == ini:
            return m
    return None


def publicar(it):
    cid = conteiner(it)
    mid = api(f"/{IG}/media_publish", {"creation_id": cid})["id"]
    info = api(f"/{mid}?fields=permalink,timestamp")
    return {"media_id": mid, "link": info.get("permalink"), "em": info.get("timestamp")}


# ---------- comandos ----------

def ler_registro():
    return json.load(open(REGISTRO, encoding="utf-8")) if os.path.exists(REGISTRO) else {}


def salvar_registro(reg):
    with open(REGISTRO, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")


def cmd_jpg():
    from PIL import Image
    n = 0
    for it in itens():
        for png in (it.get("imagens") or []) + ([it["capa"]] if it.get("capa") else []):
            dst = os.path.join(R, jpg_de(png))
            src = os.path.join(R, png)
            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=92, optimize=True, progressive=True)
            n += 1
    print(n, "JPEG gerados")


def cmd_agenda(args):
    reg = ler_registro()
    dia = args[args.index("--dia") + 1] if "--dia" in args else None
    for it in itens():
        if dia and it["post"] != dia:
            continue
        feito = reg.get(it["chave"])
        print(f"{it['quando']:%d/%m %H:%M}  {it['chave']:<10} {it['tipo']:<9} {'publicado ' + feito['link'] if feito else ''}")


def cmd_testar(args):
    alvo = args[0]
    it = next(i for i in itens() if i["chave"] == alvo)
    print("contêiner pronto, não publicado:", conteiner(it))


def cmd_devidos(args):
    aprovados = set(filter(None, args[args.index("--aprovados") + 1].split(","))) if "--aprovados" in args else set()
    agora = (datetime.datetime.fromisoformat(args[args.index("--agora") + 1]).replace(tzinfo=FUSO)
             if "--agora" in args else datetime.datetime.now(FUSO))
    seco = "--seco" in args
    reg = ler_registro()
    resumo = {"publicados": [], "pulados": [], "erros": []}
    for it in itens():
        atraso = (agora - it["quando"]).total_seconds() / 60
        if it["chave"] in reg or atraso < -5:
            continue
        if atraso > JANELA:
            if it["quando"].date() == agora.date():
                resumo["pulados"].append({"chave": it["chave"], "motivo": f"passou da janela ({it['quando']:%H:%M})"})
            continue
        if it["post"] not in aprovados:
            resumo["pulados"].append({"chave": it["chave"], "motivo": "post não aprovado no painel"})
            continue
        if seco:
            resumo["publicados"].append({"chave": it["chave"], "seco": True})
            continue
        try:
            existente = ja_no_perfil(it)
            if existente:
                reg[it["chave"]] = {"media_id": existente["id"], "link": existente.get("permalink"), "obs": "já estava no perfil"}
            else:
                reg[it["chave"]] = publicar(it)
            salvar_registro(reg)
            resumo["publicados"].append(dict(chave=it["chave"], post=it["post"], tipo=it["tipo"], **reg[it["chave"]]))
        except Exception as e:  # segue para o próximo item e relata
            resumo["erros"].append({"chave": it["chave"], "erro": str(e)})
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    return 1 if resumo["erros"] else 0


def cmd_conferir(args):
    """Checagem do dia: confere no Instagram se cada item da agenda já passou da janela e saiu."""
    agora = (datetime.datetime.fromisoformat(args[args.index("--agora") + 1]).replace(tzinfo=FUSO)
             if "--agora" in args else datetime.datetime.now(FUSO))
    reg = ler_registro()
    faltou, saiu = [], []
    for it in itens():
        if it["quando"].date() != agora.date() or (agora - it["quando"]).total_seconds() / 60 <= JANELA:
            continue
        if it["chave"] in reg:
            saiu.append(it["chave"])
            continue
        try:
            achado = ja_no_perfil(it)
        except Exception as e:  # sem conferência não dá para afirmar nada
            faltou.append({"chave": it["chave"], "horario": f"{it['quando']:%H:%M}", "erro": str(e)})
            continue
        (saiu if achado else faltou).append(it["chave"] if achado else {"chave": it["chave"], "horario": f"{it['quando']:%H:%M}"})
    print(json.dumps({"dia": f"{agora:%d/%m}", "saiu": saiu, "faltou": faltou}, ensure_ascii=False, indent=1))
    return 1 if faltou else 0


def main(argv):
    cmd, args = (argv[0], argv[1:]) if argv else ("agenda", [])
    if cmd == "jpg":
        return cmd_jpg()
    if cmd == "agenda":
        return cmd_agenda(args)
    if cmd == "testar":
        return cmd_testar(args)
    if cmd == "devidos":
        return cmd_devidos(args)
    if cmd == "conferir":
        return cmd_conferir(args)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
