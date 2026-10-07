"""Trilha do Reels D01 v2: 120 BPM, 10 compassos (20 s), com efeitos sonoros nos movimentos do vídeo.

    python3 posts/d01-teste-5-segundos/trilha_v2.py   ->   trilha-d01-v2.wav

Mesma identidade da trilha aprovada (Lá menor, Lám – Fá – Dó – Sol), com mais energia:
arpejo em semicolcheias, bateria desde o primeiro quadro e um efeito para cada movimento.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "trilhas"))
import arranjo  # noqa: E402

G = ["pad", "arpejo", "bumbo", "baixo", "chimbal"]
FICHA = {
    "bpm": 120, "tom": 9, "modo": "menor", "progressao": [0, 5, 2, 6], "nonas": True,
    "timbre_arpejo": "pluck", "passo": 0.25, "padrao_arpejo": [0, 2, 1, 3, 2, 4, 1, 3],
    "brilho": 3400, "loudness": -14.5, "semente": 21, "fade": 0.7,
    "compassos": [
        ["pad", "arpejo", "bumbo", "chimbal", "filtro"],          # 0-2   hook, abafado
        G + ["caixa", "impacto"],                                  # 2-4   "5 segundos": entra tudo
        G,                                                         # 4-6   teste 1
        G + ["caixa", "corte", "subida"],                          # 6-8   ele saiu: a bateria some
        G + ["caixa", "aberto", "melodia"],                        # 8-10  critérios
        G + ["caixa", "aberto", "melodia"],                        # 10-12
        G + ["caixa"],                                             # 12-14 teste 2
        G + ["caixa", "aberto", "melodia"],                        # 14-16 ele chamou
        ["pad", "arpejo", "subida"],                               # 16-18 virada: respiro
        G + ["caixa", "melodia", "impacto"],                       # 18-20 CTA
    ],
    "efeitos": [
        ["pop", 0.0], ["pop", 0.25], ["pop", 0.5], ["pop", 1.0], ["tique", 1.25],
        ["whoosh", 1.72], ["pop", 2.5],
        ["whoosh", 3.72],
        ["tique", 4.5], ["tique", 5.0], ["tique", 5.5], ["tique", 6.0], ["tique", 6.5],
        ["impacto", 7.0], ["glitch", 7.0],
        ["whoosh", 7.72], ["pop", 8.5], ["pop", 9.5], ["pop", 10.5],
        ["whoosh", 11.72], ["tique", 12.5], ["tique", 13.0], ["clique", 13.5], ["pop", 14.0], ["chime", 14.5],
        ["whoosh", 15.72], ["pop", 16.0], ["pop", 16.5], ["pop", 17.0], ["tique", 17.5],
        ["whoosh", 17.72], ["tique_agudo", 18.25], ["tique_agudo", 18.5], ["tique_agudo", 18.75], ["tique_agudo", 19.0],
        ["chime", 19.25],
    ],
}

if __name__ == "__main__":
    out = os.path.join(AQUI, "trilha-d01-v2.wav")
    d = arranjo.render(FICHA, out, duracao=20.0)
    print("ok", out, d)
