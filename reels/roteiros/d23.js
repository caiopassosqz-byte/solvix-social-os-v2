// D23 · Redesign em público ep. 3 (loja online fictícia). 122 BPM.
window.SPEC = { id: "D23", bpm: 122, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Numa loja online,", "a venda acontece", "[ou morre na]", "[página do produto.]"], tamanho: 106, label: "Redesign em público · ep. 3" },
  { tipo: "celular", compassos: 3, site: "loja_antes", label: "Antes · conceito", carregar: 1,
    destaques: [{ beat: 2, alvo: ".preco-x", texto: "Frete escondido.", sub: "Ele só descobre no carrinho." }, { beat: 5.5, alvo: ".comprar", texto: "Botão lá embaixo.", sub: "Sem nenhuma prova antes dele." }],
    rolar: [{ beat: 4, y: ".comprar", dur: 1.2 }], veredito: { beat: 9, titulo: "Ele fechou a aba.", sub: "Com o produto no carrinho.", tipo: "ruim" } },
  { tipo: "antesdepois", compassos: 4, antes: "loja_antes", depois: "loja_depois", label: "Redesign · conceito", revela: 1, passo: 3, decTamanho: 46,
    decisoes: ["Preço e frete à vista", "Prova perto do botão", "Botão que não some"] },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["Cada dúvida", "na página", "[é um carrinho]", "[abandonado.]"], tamanho: 128, top: 600 },
  { tipo: "cta", compassos: 2, linhas: ["Comente o", "próximo", "[segmento.]"], tamanho: 130, sub: "Projeto conceitual" }
] };
