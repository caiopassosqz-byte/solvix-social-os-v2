# D01 · Teste dos 5 segundos

- **Função:** Atração
- **Formato:** Reels, 1080×1920, 25,6 segundos
  - `reels-d01-com-trilha.mp4`: com a trilha original da Solvix
  - `reels-d01.mp4`: sem som, para escolher o áudio no app
- **Capa:** `capa.png` (o hook fica dentro do corte 3:4 da grade do perfil)
- **Métrica:** % de alcance em não seguidores + envios
- **Fonte editável:** `reels.html` (abra no navegador; `render(t)` mostra o quadro do segundo `t`)

## Roteiro

| Tempo | Cena | Texto na tela |
|---|---|---|
| 0,0 – 4,3 s | Hook. A primeira frase já aparece no quadro 0; não espere o fade para prender. | "Abra seu site no celular." → "Você tem 5 segundos." Cinco barras enchem como um cronômetro. |
| 4,3 – 10,6 s | Critérios, um por vez. | "Nesses 5 segundos, quem chega precisa entender: 01 O que você faz. 02 Para quem. 03 Como falar com você." |
| 10,7 – 19,1 s | Teste ao vivo. Dois sites de exemplo criados pela Solvix, cronômetro de 5 segundos. | Esquerda: "Bem-vindo ao nosso site" → **Não passou**. Direita: promessa clara e botão de WhatsApp → **Passou**. |
| 19,2 – 21,3 s | Virada para o espectador. | "Agora abra o seu." |
| 21,3 – 25,6 s | CTA e assinatura. | "Envie para quem tem site e nunca fez esse teste." · SOLVIX · Sites que posicionam |

## Áudio

Duas opções:

1. **Trilha original (`trilha-d01.wav`, já mixada em `reels-d01-com-trilha.mp4`).** Eletrônico minimalista a 112,5 BPM, composto em código por `trilha.py`, sem uso de música de terceiros. Os cortes do vídeo caem nos compassos:

   | Compasso | Tempo | Música | Vídeo |
   |---|---|---|---|
   | 1–2 | 0,0 – 4,3 s | Pad, arpejo e um tique por tempo | Hook; as 5 barras enchem no ritmo dos tiques |
   | 3–5 | 4,3 – 10,7 s | Entram bumbo e baixo | Critérios, um a cada 2 tempos |
   | 6–8 | 10,7 – 17,1 s | Entram chimbal e palmas; ruído sobe no compasso 8 | Teste ao vivo e cronômetro |
   | 9 | 17,1 s | Impacto | Veredito: "Não passou" / "Passou" |
   | 10 | 19,2 – 21,3 s | Respiro: só pad e arpejo | "Agora abra o seu." |
   | 11–12 | 21,3 – 25,6 s | Groove volta e sai em fade | CTA e assinatura |

   Volume entregue em −16 LUFS, pico −1,5 dB. Para gerar de novo: `python3 trilha.py`.

2. **Áudio da biblioteca do Instagram.** Suba `reels-d01.mp4` e escolha um instrumental eletrônico minimalista entre 95 e 115 BPM, com volume em torno de 20%. Ligar o Reels a um áudio da biblioteca ajuda na descoberta pela página do áudio.

## Legenda

Abra seu site no celular. Você tem 5 segundos.

Nesse tempo, quem chega precisa entender três coisas: o que você faz, para quem e como falar com você. Se uma delas falta, a pessoa volta para a busca e encontra outra empresa.

Faça o teste agora e conte nos comentários: passou ou não?

Solvix Agency · sites que posicionam.

#criacaodesites #landingpage #sitesprofissionais #presencadigital #empreendedorismo

## Versão falada (opcional)

Para gravar com rosto, mantenha o mesmo texto na tela e use esta fala, no mesmo ritmo:

> Abra seu site no celular. Agora. Você tem cinco segundos.
> Nesse tempo, quem chega precisa entender o que você faz, para quem, e como falar com você.
> Esse aqui não passa: "bem-vindo ao nosso site" não diz nada.
> Esse passa: promessa clara e o botão do WhatsApp na primeira tela.
> Agora abre o seu. Passou? Manda esse vídeo pra quem tem site e nunca fez esse teste.

Grave na vertical, com luz lateral e fundo neutro escuro, para manter o padrão da marca.
