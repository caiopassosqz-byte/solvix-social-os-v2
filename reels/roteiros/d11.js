// D11 · O botão do WhatsApp. 104 BPM.
window.SPEC = { id: "D11", bpm: 104, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["O botão mais", "importante do", "seu site está", "[escondido.]"], tamanho: 128 },
  { tipo: "celular", compassos: 3, site: "whats_escondido", label: "Onde está o WhatsApp?", carregar: 1,
    rolar: [{ beat: 2, y: 700, dur: 1 }, { beat: 3.5, y: ".wz", dur: 1 }],
    destaques: [{ beat: 5, alvo: ".wz", texto: "Só no rodapé.", sub: "Quem não rola até o fim nunca vê." }],
    veredito: { beat: 8.5, titulo: "Ele desistiu.", sub: "Antes de chegar lá.", tipo: "ruim" } },
  { tipo: "celular", compassos: 3, site: "whats_fixo", label: "Depois · demonstração", entrada: "direita",
    destaques: [{ beat: 1.5, alvo: ".sticky", texto: "Fixo na tela.", sub: "Aparece desde o primeiro segundo." }],
    toque: { beat: 4, alvo: ".sticky" }, mensagem: { beat: 5, texto: "Olá! Vim pelo site e quero um orçamento." },
    veredito: { beat: 7, titulo: "Ele chamou.", sub: "Sem rolar nada.", tipo: "bom" } },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "Três ajustes", itens: ["Fixo na tela.", "Mensagem pronta.", "Na primeira tela."], tamanho: 104, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["Manda para quem", "recebe contato", "[pelo site.]"], tamanho: 112 }
] };
