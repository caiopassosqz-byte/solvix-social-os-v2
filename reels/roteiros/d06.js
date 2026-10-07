// D06 · Site decorativo x site que vende. 116 BPM.
window.SPEC = { id: "D06", bpm: 116, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Seu site", "é bonito.", "[Mas ele vende?]"], tamanho: 150 },
  { tipo: "celular", compassos: 4, site: "decorativo", label: "Site decorativo · demonstração", carregar: 4,
    destaques: [{ beat: 5, alvo: ".slider h4", texto: "Não diz o que faz.", sub: "“Inovação que transforma” serve para qualquer empresa." },
                { beat: 9.5, alvo: ".contato", texto: "Esconde o contato.", sub: "Só no rodapé, sem WhatsApp." }],
    rolar: [{ beat: 8, y: ".contato", dur: 1.2 }], veredito: { beat: 13, titulo: "Ele não comprou.", sub: "Achou bonito e foi embora.", tipo: "ruim" } },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "3 sinais de site decorativo", itens: ["Não diz o que faz.", "Esconde o contato.", "Demora para abrir."], tamanho: 96, passo: 3 },
  { tipo: "celular", compassos: 3, site: "moderno", label: "Site que vende · demonstração", entrada: "direita", carregar: 1,
    destaques: [{ beat: 2, alvo: "h3", texto: "Diz o que faz.", sub: "Serviço, para quem e como." }],
    toque: { beat: 5, alvo: "#wbtn" }, mensagem: { beat: 6, texto: "Oi! Quero um orçamento para meu apartamento." },
    veredito: { beat: 8, titulo: "Esse vende.", sub: "Bonito e claro ao mesmo tempo.", tipo: "bom" } },
  { tipo: "cta", compassos: 2, linhas: ["Manda para quem", "[acabou de fazer]", "[um site.]"], tamanho: 112 }
] };
