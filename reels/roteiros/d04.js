// D04 · Redesign em público ep. 1 (clínica fictícia). 124 BPM, 12 compassos.
window.SPEC = { id: "D04", bpm: 124, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Mesma empresa.", "Mesmo serviço.", "[Só mudamos a]", "[primeira tela.]"], tamanho: 124, label: "Redesign em público · ep. 1" },
  { tipo: "celular", compassos: 3, site: "clinica_antes", label: "Antes · conceito", carregar: 1.5,
    destaques: [{ beat: 2, alvo: "h3", texto: "Não diz o que faz.", sub: "Só dá boas-vindas." }, { beat: 5.5, alvo: ".contato", texto: "O botão está no fim.", sub: "Depois de três rolagens." }],
    rolar: [{ beat: 4, y: ".contato", dur: 1.2 }], veredito: { beat: 9, titulo: "Ele saiu.", sub: "Antes de achar o botão.", tipo: "ruim" } },
  { tipo: "antesdepois", compassos: 3, antes: "clinica_antes", depois: "clinica_depois", label: "Redesign · conceito", revela: 1.5, passo: 2,
    decisoes: ["Promessa no título", "Botão na primeira tela", "Foto que mostra o resultado"] },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["A primeira tela", "[decide se a]", "[pessoa fica.]"], tamanho: 136, top: 620 },
  { tipo: "cta", compassos: 2, linhas: ["Comente o", "segmento do", "[próximo redesign.]"], tamanho: 112, sub: "Projeto conceitual" }
] };
