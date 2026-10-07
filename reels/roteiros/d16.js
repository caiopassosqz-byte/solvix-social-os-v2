// D16 · Teste dos 5 segundos ep. 2: três sites conceituais. 112 BPM.
window.SPEC = { id: "D16", bpm: 112, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Fiz o teste dos", "5 segundos", "em 3 sites.", "[Só um passou.]"], tamanho: 120, label: "Teste dos 5 segundos · ep. 2" },
  { tipo: "celular", compassos: 2, site: "testeA", label: "Site 1 · conceito", carregar: 1, contador: { de: 5, ate: 0, inicio: 1, passo: 1 },
    veredito: { beat: 6.5, titulo: "Não passou.", sub: "Não diz o que faz.", tipo: "ruim" } },
  { tipo: "celular", compassos: 2, site: "testeB", label: "Site 2 · conceito", entrada: "direita", carregar: 1, contador: { de: 5, ate: 0, inicio: 1, passo: 1 },
    veredito: { beat: 6.5, titulo: "Não passou.", sub: "Diz o que faz, mas esconde o contato.", tipo: "ruim" } },
  { tipo: "celular", compassos: 2, site: "testeC", label: "Site 3 · conceito", entrada: "esquerda", carregar: 0.5, contador: { de: 5, ate: 3, inicio: 1, passo: 1 },
    toque: { beat: 3.5, alvo: "#wbtn" }, mensagem: { beat: 4.5, texto: "Oi! Quero agendar uma avaliação." },
    veredito: { beat: 5.5, titulo: "Passou.", sub: "O quê, para quem e como chamar.", tipo: "bom" } },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "Em 5 segundos, ele precisa entender", itens: ["O que você faz.", "Para quem.", "Como te chamar."], tamanho: 104, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["E o seu,", "[passaria?]"], tamanho: 150, sub: "Comente aqui" }
] };
