# Solvix Social OS

Painel de criação de conteúdo do Instagram da Solvix Agency.

Abra `index.html` no navegador. Não precisa de instalação nem de build.

## Abas

- **Visão geral:** objetivo do ciclo, as 3 métricas, a proporção entre funções, os próximos posts e os gargalos de partida.
- **Calendário:** os 30 posts com dia, função, objetivo, pilar, tema, ângulo, hook, formato, ideia central, CTA e métrica. Cada post tem uma prévia da capa no padrão da marca, um status (Planejado, Em produção, Publicado) e um campo para registrar o resultado.
- **Hooks:** 30 ganchos no tom editorial direto, agrupados por mecanismo.
- **Cérebro da marca:** posicionamento, valores, tom de voz, serviços, pilares e regras visuais do manual.
- **Rotina:** preparação antes do D01, stories diários e revisão semanal.

O status e as anotações ficam salvos no navegador onde foram feitos. A data de início do ciclo pode ser alterada no calendário.

O contexto da marca e as regras de conteúdo estão em `CONTEXTO.md`.

## Trilhas dos Reels

Cada Reels tem uma música original própria, gerada por `trilhas/gerador.py` a partir de `trilhas/catalogo.json` (tom, modo, andamento, acordes, timbres e batida por faixa). As prévias em MP3 ficam em `trilhas/demos/`; os WAV gerados em `trilhas/saida/` não vão para o repositório.

```
python3 trilhas/gerador.py gerar D04     # uma faixa
python3 trilhas/gerador.py gerar todos   # todas as faixas em rascunho
```

Quando o vídeo de um Reels fica pronto, ajuste as `secoes` da faixa no catálogo para as viradas caírem nos cortes e gere de novo. Faixas com `"status": "aprovada"` não são regeradas.
