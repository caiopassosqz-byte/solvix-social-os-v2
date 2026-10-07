# Solvix Social OS

Painel de criação de conteúdo do Instagram da Solvix Agency.

Abra `index.html` no navegador. Não precisa de instalação nem de build.

## Áreas do painel

- **Hoje:** quanto falta para o próximo post, o mapa dos 30 dias com a etapa de cada um, o que precisa de você (aprovações e pendências), a atividade recente e como funciona a publicação.
- **Calendário:** visão de mês ou lista, com filtro por função e formato.
- **Produção:** quadro com as seis etapas (Planejado, Em produção, Para aprovar, Aprovado, Agendado, Publicado).
- **Grid:** o perfil como vai ficar ao fim do ciclo, com os fixados no topo.
- **Biblioteca:** peças prontas, trilhas dos Reels e banco de hooks.
- **Estratégia** e **Marca:** objetivo, métricas, proporção, linha editorial, rotina, ajustes do ciclo e regras da marca.

Clicar em qualquer post abre a ficha: peça final (slides ou vídeo), trilha, legenda com botão de copiar, plano, botões **Aprovar** e **Pedir ajuste**, resultado e comentário.

Aberto pelo link do Claude, o painel sincroniza: aprovações, pedidos de ajuste, pendências e resultados ficam salvos num banco que o Claude lê. Aberto como arquivo local, salva só no navegador.

## Como atualizar o painel

O `index.html` é gerado. Edite as fontes e monte de novo:

- `painel/plano.json`: os 30 posts, pilares, funções, hooks e paleta.
- `painel/modelo.html`: visual e comportamento.
- `painel/montar.py`: junta plano, peças e legendas das pastas `posts/dNN-*` (lidas sozinhas: `reels-dNN.mp4` + `capa.png`, ou `slide-NN.png`, e a seção `## Legenda` de `roteiro.md` ou `legenda.md`), trilhas e pendências.

```
python3 painel/montar.py
```

## Trilhas dos Reels

Cada Reels tem uma música original própria, gerada por `trilhas/gerador.py` a partir de `trilhas/catalogo.json` (tom, modo, andamento, acordes, timbres e batida por faixa). As prévias em MP3 ficam em `trilhas/demos/`; os WAV gerados em `trilhas/saida/` não vão para o repositório.

```
python3 trilhas/gerador.py gerar D04     # uma faixa
python3 trilhas/gerador.py gerar todos   # todas as faixas em rascunho
```

Quando o vídeo de um Reels fica pronto, ajuste as `secoes` da faixa no catálogo para as viradas caírem nos cortes e gere de novo. Faixas com `"status": "aprovada"` não são regeradas.

## Motor de Reels

Os Reels do D04 em diante saem de um motor só: `reels/motor.html` desenha cada quadro a partir de um roteiro em `reels/roteiros/dNN.js` (cenas, compassos, textos, telas de site e efeitos). As telas de site dentro do celular ficam em `reels/sites.js`; todas são de empresas fictícias e aparecem identificadas como demonstração ou conceito.

```
reels/gerar.sh d04 d04-redesign-clinica   # vídeo, trilha, vídeo com som, prévia MP3 e capa
```

A trilha de cada Reels (`reels/trilha.py`) usa a harmonia da faixa no catálogo, o andamento do roteiro e põe um efeito sonoro em cada movimento do vídeo. Regras do motor: o preto domina, no máximo uma cena clara por vídeo, texto dentro da zona segura.

## Motor de carrosséis

`carrosseis/motor.html?c=d05` monta os slides de 1080×1350 a partir de `carrosseis/roteiros/dNN.js`. O mesmo motor gera os PDFs dos materiais.

```
node carrosseis/exportar.js d05 posts/d05-checklist-landing-page
node carrosseis/exportar.js checklist /tmp/x materiais/checklist-landing-page.pdf
```

## Materiais e integração

- `materiais/`: o que enviar para quem manda CHECKLIST, PREÇO ou ANÁLISE na DM, com respostas prontas.
- `INTEGRACAO.md`: como conectar o Instagram da Solvix para a publicação automática.
