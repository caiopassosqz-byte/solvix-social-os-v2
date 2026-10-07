// Material: guia de investimento (enviado a quem manda PREÇO na DM). PDF de 6 páginas.
// Só usa a faixa geral confirmada (R$1 mil a R$35 mil). Faixas por tipo: adicionar quando a Solvix definir.
window.CAR = { id: "PRECO", pdf: true, slides: [
  { tipo: "capa", eyebrow: "Material Solvix · Guia de investimento", titulo: "Quanto custa um site. [Sem rodeio.]", tamanho: 110, rodape: "Solvix Agency", rodapeDir: "Edição 2026" },
  { tipo: "escada", eyebrow: "01 · A faixa", titulo: "De R$1 mil [a R$35 mil.]", min: "a partir de R$1 mil", max: "até R$35 mil",
    degraus: [{ nome: "Landing page", desc: "uma página, um objetivo" }, { nome: "Site institucional", desc: "a empresa inteira" }, { nome: "E-commerce", desc: "catálogo, pagamento e frete" }, { nome: "Sistema sob medida", desc: "as regras do seu negócio" }],
    nota: "O valor exato depende do escopo e vem por escrito na proposta." },
  { tipo: "linhas", eyebrow: "02 · O que muda o preço", titulo: "Quatro fatores.", tamanho: 80, itens: [
    { t: "Páginas", d: "Uma página com um objetivo custa menos que a empresa inteira apresentada." },
    { t: "Integrações", d: "WhatsApp, agenda, pagamento, CRM e outros sistemas conectados." },
    { t: "Conteúdo", d: "Textos e fotos prontos, ou escritos e produzidos do zero." },
    { t: "Estratégia", d: "Quanto estudo de cliente, oferta e estrutura vem antes do layout." }] },
  { tipo: "linhas", eyebrow: "03 · Para escolher", titulo: "Qual faz sentido [para você.]", tamanho: 76, compacta: true, itens: [
    { t: "Landing page", d: "Um serviço ou uma oferta, com anúncio ou tráfego do Instagram." },
    { t: "Site institucional", d: "Vários serviços e clientes que pesquisam antes de chamar." },
    { t: "E-commerce", d: "Produto com estoque, frete e pagamento online." },
    { t: "Sistema sob medida", d: "Processos internos, clientes e pedidos num lugar só." }] },
  { tipo: "checks", eyebrow: "04 · Em todo projeto", titulo: "O que vem junto.", tamanho: 64, claro: true, itens: [
    { t: "Proposta com escopo, prazo e valor por escrito" }, { t: "Domínio no nome da sua empresa" }, { t: "Testes no celular antes de publicar" }, { t: "Acesso a todos os arquivos e painéis" }, { t: "Suporte depois da entrega" }] },
  { tipo: "cta", eyebrow: "Próximo passo", titulo: "Vamos chegar ao valor [do seu projeto?]", sub: "Responda a mensagem com o tipo de site e o que ele precisa fazer. A proposta vem por escrito.", botoes: ["Responder na DM"], rodape: "Solvix Agency", rodapeDir: "Sites que posicionam" }
] };
