// D03 · Por que a Solvix existe. Manifesto animado, sem rosto e sem voz. 104 BPM.
window.SPEC = { id: "D03", bpm: 104, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["A Solvix não", "nasceu para", "fazer site", "[bonito.]"], tamanho: 136, label: "Construindo a Solvix" },
  { tipo: "celular", compassos: 3, site: "decorativo", label: "Site bonito · demonstração", carregar: 1.5,
    destaques: [{ beat: 2.5, alvo: ".slider h4", texto: "Bonito.", sub: "Mas não diz o que faz." }, { beat: 6, alvo: ".contato", texto: "Contato escondido.", sub: "Só no rodapé." }],
    rolar: [{ beat: 5, y: ".contato", dur: 1 }], veredito: { beat: 9, titulo: "Ninguém chamou.", sub: "Achou bonito e foi embora.", tipo: "ruim" } },
  { tipo: "palavras", compassos: 2, linhas: ["Site bonito", "[qualquer um faz.]"], tamanho: 150, top: 640 },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "A Solvix existe para", itens: ["Clareza.", "Estrutura.", "Resultado."], tamanho: 130, passo: 3 },
  { tipo: "celular", compassos: 3, site: "moderno", label: "Site que trabalha · demonstração", entrada: "direita", carregar: 0.5,
    destaques: [{ beat: 1.5, alvo: "h3", texto: "Diz o que faz.", sub: "Para quem e como chamar." }],
    toque: { beat: 4, alvo: "#wbtn" }, mensagem: { beat: 5, texto: "Oi! Vi o site e quero um orçamento." },
    veredito: { beat: 7, titulo: "Esse trabalha.", sub: "Em segundos, sem rolar a página.", tipo: "bom" } },
  { tipo: "cta", compassos: 2, linhas: ["Siga para", "acompanhar a", "[construção da Solvix.]"], tamanho: 112 }
] };
