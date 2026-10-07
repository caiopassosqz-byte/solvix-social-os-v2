// D26 · Site desatualizado. 108 BPM.
window.SPEC = { id: "D26", bpm: 108, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Seu site foi", "feito em 2019.", "[Seu cliente]", "[percebe.]"], tamanho: 136 },
  { tipo: "celular", compassos: 4, site: "antigo2019", label: "Site antigo · demonstração", carregar: 1,
    destaques: [{ beat: 1.5, alvo: ".quebra", texto: "Quebra no celular.", sub: "O texto passa da tela." },
                { beat: 5, alvo: ".stock", texto: "Foto de banco de imagem.", sub: "Ele já viu essa foto em outro site." },
                { beat: 8.5, alvo: ".form", texto: "Formulário sem resposta.", sub: "Ninguém sabe quando vai ter retorno." },
                { beat: 12, alvo: ".rodape", texto: "© 2019 no rodapé.", sub: "Parece que ninguém cuida." }],
    rolar: [{ beat: 4, y: ".stock", dur: 1 }, { beat: 7.5, y: ".form", dur: 1 }, { beat: 11, y: ".rodape", dur: 1 }] },
  { tipo: "antesdepois", compassos: 3, antes: "antigo2019", depois: "moderno", label: "Atualizado · demonstração", revela: 1, passo: 2,
    decisoes: ["Feito para o celular", "Fotos reais", "Contato que responde"] },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["Ele não vê", "o ano.", "[Ele sente.]"], tamanho: 160, top: 600 },
  { tipo: "cta", compassos: 2, linhas: ["Manda para quem", "[precisa ouvir isso.]"], tamanho: 116 }
] };
