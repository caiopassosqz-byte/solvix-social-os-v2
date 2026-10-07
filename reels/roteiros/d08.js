// D08 · Busca pelo serviço. 104 BPM.
window.SPEC = { id: "D08", bpm: 104, cenas: [
  { tipo: "palavras", compassos: 2, linhas: ["Seu cliente", "não pesquisa", "[seu nome.]"], tamanho: 150 },
  { tipo: "busca", compassos: 4, label: "A busca de quem ainda não te conhece",
    digitar: [{ texto: "Clínica Sorrir", beat: 1, riscar: true }, { texto: "dentista perto de mim", beat: 4.5 }],
    resultadosBeat: 7, resultados: [
      { nome: "Odonto Centro", linha: "4,8 ★ · Dentista · aberto agora", tag: "Site · Rotas · Ligar" },
      { nome: "Clínica Prisma", linha: "4,7 ★ · Clínica odontológica", tag: "Site · Rotas · Ligar" },
      { nome: "Sorriso Pleno", linha: "4,9 ★ · Dentista", tag: "Site · Rotas" }],
    veredito: { beat: 11, titulo: "Você não apareceu.", sub: "Ele vai escolher entre esses três.", tipo: "ruim" } },
  { tipo: "palavras", compassos: 2, claro: true, linhas: ["Ele pesquisa", "[o que você faz.]"], tamanho: 150, top: 640 },
  { tipo: "lista", compassos: 3, eyebrow: "Para aparecer nessa busca", itens: ["Perfil no Google.", "Site que diz o serviço.", "Um levando ao outro."], tamanho: 88, passo: 3 },
  { tipo: "cta", compassos: 2, linhas: ["Manda para", "um amigo", "[empresário.]"], tamanho: 130 }
] };
