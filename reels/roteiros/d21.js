// D21 · Texto do site: adjetivo x fato. 109 BPM.
window.SPEC = { id: "D21", bpm: 109, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["“Qualidade e", "excelência”", "[não diz nada.]"], tamanho: 140 },
  { tipo: "celular", compassos: 2, site: "texto_antes", label: "Contabilidade · conceito", carregar: 1,
    destaques: [{ beat: 2, alvo: "h3", texto: "Seu cliente pulou.", sub: "Todo site diz isso." }] },
  { tipo: "reescrita", compassos: 4, eyebrow: "Adjetivo vira fato", passo: 5, inicio: 0.5, pares: [
    { antes: "Qualidade e excelência em contabilidade.", depois: "Contabilidade para MEI e ME, com resposta no mesmo dia." },
    { antes: "Soluções completas para sua empresa.", depois: "Abrimos sua empresa e cuidamos dos impostos todo mês." },
    { antes: "Atendimento diferenciado.", depois: "Um contador fixo para você, pelo WhatsApp." }] },
  { tipo: "lista", compassos: 3, claro: true, eyebrow: "Troque o adjetivo por", itens: ["O que você faz.", "Para quem.", "Em quanto tempo."], tamanho: 104, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["Comente a primeira", "frase do seu site.", "[Eu reescrevo.]"], tamanho: 100 }
] };
