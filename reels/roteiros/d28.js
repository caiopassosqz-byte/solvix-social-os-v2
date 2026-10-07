// D28 · Barato que sai caro. 107 BPM.
window.SPEC = { id: "D28", bpm: 107, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["O site de R$300", "[costuma custar]", "[duas vezes.]"], tamanho: 128, label: "Investimento sem rodeio" },
  { tipo: "numero", compassos: 2, antes: "Você paga", numero: "2×", depois: "pelo mesmo site.", depoisTamanho: 112, tamanho: 760 },
  { tipo: "lista", compassos: 4, eyebrow: "Onde o barato sai caro", itens: ["Refazer do zero.", "Domínio no nome de outro.", "Sem suporte depois."], tamanho: 96, passo: 4 },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["Barato é o que", "funciona na", "[primeira vez.]"], tamanho: 140, top: 600 },
  { tipo: "cta", compassos: 2, linhas: ["Manda para quem", "está pedindo", "[orçamento.]"], tamanho: 120 }
] };
