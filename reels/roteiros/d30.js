// D30 · 30 dias em números. Prestação de contas do ciclo. 110 BPM.
// PENDENTE: preencher NUMEROS com os dados reais do ciclo antes de renderizar. Mesmo que sejam pequenos, são os reais.
var NUMEROS = { seguidores: "—", alcance: "—", pedidos: "—", reunioes: "—" };
window.SPEC = { id: "D30", bpm: 110, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["30 dias atrás:", "[0 seguidores.]"], tamanho: 150, label: "Construindo em público" },
  { tipo: "numero", compassos: 2, antes: "Seguidores hoje", numero: NUMEROS.seguidores, depois: "", tamanho: 520 },
  { tipo: "numero", compassos: 2, antes: "Contas alcançadas", numero: NUMEROS.alcance, depois: "", tamanho: 420 },
  { tipo: "numero", compassos: 2, antes: "Pedidos na DM (CHECKLIST, PREÇO, ANÁLISE)", numero: NUMEROS.pedidos, depois: "", tamanho: 420 },
  { tipo: "numero", compassos: 2, claro: true, antes: "Reuniões", numero: NUMEROS.reunioes, depois: "", tamanho: 520 },
  { tipo: "lista", compassos: 3, eyebrow: "No próximo ciclo", itens: ["[preencher]", "[preencher]", "[preencher]"], tamanho: 96, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["Siga para acompanhar", "[os próximos 30 dias.]"], tamanho: 112 }
] };
