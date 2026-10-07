// D19 · Perfil no Google. 115 BPM.
window.SPEC = { id: "D19", bpm: 115, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Seu perfil no", "Google é a", "primeira página", "[do seu site.]"], tamanho: 128 },
  { tipo: "celular", compassos: 4, site: "perfil", label: "Perfil de empresa · demonstração", carregar: 1,
    destaques: [{ beat: 2, alvo: ".cat", texto: "Categoria certa.", sub: "É por ela que você aparece na busca." },
                { beat: 6, alvo: ".fotos", texto: "Fotos atuais.", sub: "O lugar como ele é hoje." },
                { beat: 10, alvo: ".bsite", texto: "Link para a página certa.", sub: "A que fala do serviço buscado." }],
    toque: { beat: 13, alvo: ".bsite" } },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["E ninguém", "[cuida dela.]"], tamanho: 160, top: 660 },
  { tipo: "palavras", compassos: 2, linhas: ["Perfil e site", "[trabalham juntos.]"], tamanho: 140, top: 640 },
  { tipo: "cta", compassos: 2, linhas: ["Manda para quem", "tem negócio", "[físico.]"], tamanho: 120 }
] };
