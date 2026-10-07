// D13 · Construindo em público: os números das duas primeiras semanas. 82 BPM no catálogo; aqui 110 para acompanhar o movimento.
// PENDENTE: preencher NUMEROS com os dados reais do Insights (até o D12) antes de renderizar. Nada aqui pode ser estimado.
var NUMEROS = { seguidores: "—", alcance: "—", naoSeguidores: "—", mensagens: "—" };
window.SPEC = { id: "D13", bpm: 110, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Comecei o Instagram", "da Solvix com", "[0 seguidores.]"], tamanho: 128, label: "Construindo em público" },
  { tipo: "palavras", compassos: 1, linhas: ["Vou mostrar", "[tudo.]"], tamanho: 170, top: 640 },
  { tipo: "numero", compassos: 2, antes: "Seguidores em 12 dias", numero: NUMEROS.seguidores, depois: "", tamanho: 520 },
  { tipo: "numero", compassos: 2, antes: "Contas alcançadas", numero: NUMEROS.alcance, depois: "", tamanho: 420 },
  { tipo: "numero", compassos: 2, claro: true, antes: "Vindas de quem não segue", numero: NUMEROS.naoSeguidores, depois: "", tamanho: 420 },
  { tipo: "lista", compassos: 3, eyebrow: "O que muda a partir daqui", itens: ["[preencher]", "[preencher]", "[preencher]"], tamanho: 96, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["Siga para ver", "[os próximos números.]"], tamanho: 120 }
] };
