// D14 · Redesign em público ep. 2 (academia fictícia). 124 BPM.
window.SPEC = { id: "D14", bpm: 124, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Redesenhei a", "página de uma", "academia em", "[3 decisões.]"], tamanho: 128, label: "Redesign em público · ep. 2" },
  { tipo: "celular", compassos: 2, site: "academia_antes", label: "Antes · conceito", carregar: 1,
    destaques: [{ beat: 2, alvo: "h3", texto: "Não diz onde nem quando.", sub: "Nem quanto custa." }] },
  { tipo: "antesdepois", compassos: 4, antes: "academia_antes", depois: "academia_depois", label: "Redesign · conceito", revela: 1, passo: 3, decTamanho: 44,
    decisoes: ["Horário e unidade no topo", "Aula experimental como oferta", "Planos sem letras miúdas"] },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["Outro segmento.", "[Mesmo método.]"], tamanho: 136, top: 660 },
  { tipo: "cta", compassos: 2, linhas: ["Comente o", "segmento do", "[próximo redesign.]"], tamanho: 112, sub: "Projeto conceitual" }
] };
