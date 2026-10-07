// D10 · Quanto custa um site. 110 BPM (o catálogo previa uma faixa lenta; o vídeo pede movimento).
window.SPEC = { id: "D10", bpm: 110, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Um site pode", "custar", "[R$1 mil ou]", "[R$35 mil.]"], tamanho: 136, label: "Investimento sem rodeio" },
  { tipo: "escada", compassos: 4, eyebrow: "Do mais simples ao mais completo", passo: 2, min: "a partir de R$1 mil", max: "até R$35 mil",
    degraus: [{ nome: "Landing page", desc: "uma página, um objetivo" }, { nome: "Site institucional", desc: "a empresa inteira" },
              { nome: "E-commerce", desc: "catálogo, pagamento e frete" }, { nome: "Sistema sob medida", desc: "as regras do seu negócio" }] },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "O que muda o preço", itens: ["Páginas.", "Integrações.", "Conteúdo.", "Estratégia."], tamanho: 110, passo: 2 },
  { tipo: "palavras", compassos: 2, linhas: ["Você paga pelo", "que o site", "[precisa fazer.]"], tamanho: 136 },
  { tipo: "cta", compassos: 2, linhas: ["Envie PREÇO", "[na DM.]"], tamanho: 150, sub: "E receba o guia de investimento" }
] };
