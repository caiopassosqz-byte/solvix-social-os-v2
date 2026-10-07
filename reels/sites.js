/* Telas de site usadas dentro do celular dos Reels. Todas são demonstrações:
   empresas fictícias, criadas pela Solvix para explicar uma ideia. Largura útil da tela: 424 px. */
(function () {
  var css = [
    ".site .foto { height: 300px; border-radius: 18px; position: relative; overflow: hidden; }",
    ".site .foto::before { content: ''; position: absolute; width: 260px; height: 260px; border-radius: 50%; right: -40px; top: -60px; background: rgba(255,255,255,0.22); }",
    ".site .foto::after { content: ''; position: absolute; left: 24px; bottom: 22px; width: 150px; height: 10px; border-radius: 5px; background: rgba(255,255,255,0.55); box-shadow: 0 -22px 0 -2px rgba(255,255,255,0.35); }",
    ".site .foto.clinica { background: linear-gradient(140deg, #24413F 0%, #5E8580 55%, #C9D8D3 100%); }",
    ".site .foto.academia { background: linear-gradient(140deg, #1B1B1B 0%, #4A3A2C 60%, #B88A5A 100%); }",
    ".site .foto.loja { background: radial-gradient(circle at 50% 55%, #E9E2D6 0 34%, #CFC4B2 35% 100%); }",
    ".site .foto.loja::after, .site .foto.loja::before { display: none; }",
    ".site .foto .obj { position: absolute; left: 50%; top: 50%; width: 150px; height: 190px; border-radius: 26px 26px 40px 40px; background: linear-gradient(160deg, #3B4A3F, #1E2722); transform: translate(-50%, -46%); box-shadow: 0 30px 40px rgba(0,0,0,0.25); }",
    ".site .foto.studio { background: linear-gradient(140deg, #2B2A28 0%, #6B655C 60%, #D9D2C5 100%); }",
    ".site .foto.cinza { background: linear-gradient(135deg, #CFCFCC, #E2E2DF); }",
    ".site .foto.cinza::before, .site .foto.cinza::after { display: none; }",
    ".site .banco { height: 260px; border-radius: 4px; background: linear-gradient(180deg, #DCE6EE, #B9C9D6); position: relative; overflow: hidden; }",
    ".site .banco i { position: absolute; bottom: -30px; width: 110px; height: 190px; border-radius: 55px 55px 0 0; background: #8FA3B4; }",
    ".site .banco i::before { content: ''; position: absolute; left: 25px; top: -66px; width: 60px; height: 60px; border-radius: 50%; background: #8FA3B4; }",
    ".site .marca { position: absolute; left: 50%; top: 40%; transform: translate(-50%, -50%) rotate(-18deg); font-size: 34px; font-weight: 700; color: rgba(255,255,255,0.55); letter-spacing: 0.1em; }",
    ".site .pill { display: inline-block; font-size: 17px; font-weight: 600; letter-spacing: 0.06em; padding: 8px 14px; border-radius: 999px; background: #EAEAE6; color: #333; margin-right: 8px; }",
    ".site .info { display: flex; gap: 10px; flex-wrap: wrap; }",
    ".site .preco { display: flex; align-items: baseline; gap: 14px; }",
    ".site .preco b { font-size: 46px; font-weight: 700; letter-spacing: -0.02em; }",
    ".site .preco span { font-size: 20px; color: #575757; }",
    ".site .stars { font-size: 21px; color: #333; }",
    ".site .plano { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-radius: 14px; box-shadow: inset 0 0 0 2px #E2E2DF; font-size: 22px; }",
    ".site .plano b { font-size: 26px; }",
    ".site .slider { height: 520px; border-radius: 0; margin: 0 -40px; background: linear-gradient(160deg, #191919 0%, #3D3D3D 50%, #9A9A96 100%); position: relative; }",
    ".site .slider .dots { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }",
    ".site .slider .dots i { width: 12px; height: 12px; border-radius: 50%; background: rgba(255,255,255,0.5); }",
    ".site .slider .dots i:first-child { background: #fff; }",
    ".site .slider h4 { position: absolute; left: 40px; right: 40px; bottom: 80px; color: #fff; font-family: var(--serif); font-weight: 300; font-size: 50px; line-height: 1.05; }",
    ".site .foot { margin: 20px -40px -40px; padding: 30px 40px 40px; background: #1A1A1A; color: #A3A3A3; font-size: 19px; display: grid; gap: 12px; }",
    ".site .foot b { color: #F5F5F3; font-size: 22px; }",
    ".site .foot .wz, .site .foot .contato { color: #F5F5F3; font-size: 20px; text-decoration: underline; }",
    ".site.velho { padding: 96px 14px 14px; gap: 12px; font-family: 'Times New Roman', serif; }",
    ".site.velho .topo { background: #2C4E86; color: #fff; padding: 14px; font-size: 26px; font-weight: 700; display: flex; justify-content: space-between; }",
    ".site.velho .menu { display: flex; gap: 0; font-size: 15px; white-space: nowrap; overflow: hidden; }",
    ".site.velho .menu span { background: #E6E6E6; border: 1px solid #BBB; padding: 6px 12px; }",
    ".site.velho .quebra { width: 640px; font-size: 30px; color: #2C4E86; font-weight: 700; }",
    ".site.velho p { font-family: 'Times New Roman', serif; font-size: 17px; color: #333; }",
    ".site.velho .form { border: 1px solid #AAA; padding: 12px; display: grid; gap: 8px; font-size: 16px; color: #555; }",
    ".site.velho .form i { display: block; height: 26px; border: 1px solid #BBB; background: #fff; }",
    ".site.velho .form u { display: inline-block; background: #DDD; border: 1px solid #999; padding: 4px 10px; text-decoration: none; width: max-content; }",
    ".site.velho .rodape { background: #DDD; font-size: 15px; color: #666; padding: 12px; text-align: center; }",
    ".site .perfil-top { display: grid; gap: 10px; padding-bottom: 6px; }",
    ".site .perfil-top h3 { font-size: 46px; }",
    ".site .cat { font-size: 21px; color: #333; width: max-content; padding: 4px 0; }",
    ".site .acoes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }",
    ".site .acoes span { text-align: center; font-size: 19px; font-weight: 600; padding: 16px 0; border-radius: 999px; box-shadow: inset 0 0 0 2px #0A0A0A; }",
    ".site .acoes span.bsite { background: #0A0A0A; color: #F5F5F3; }",
    ".site .fotos { display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 130px 130px; gap: 8px; }",
    ".site .fotos i { border-radius: 12px; background: linear-gradient(140deg, #2B2A28, #8A8174); }",
    ".site .fotos i:first-child { grid-row: span 2; background: linear-gradient(140deg, #3A3631, #C8BCA8); }",
    ".site .fotos i:nth-child(3) { background: linear-gradient(140deg, #5C574F, #DCD4C6); }",
    ".site .hor { font-size: 20px; color: #1E7B45; font-weight: 600; }",
    ".site .aval { display: grid; gap: 8px; padding: 18px; border-radius: 14px; background: #EDEDEA; font-size: 19px; color: #444; }",
    ".site .sel { font-size: 15px; letter-spacing: 0.1em; text-transform: uppercase; color: #777; font-weight: 600; }",
    ".site .faixa { background: #0A0A0A; color: #F5F5F3; margin: 0 -40px; padding: 14px 40px; font-size: 19px; font-weight: 600; letter-spacing: 0.04em; }"
  ].join("\n");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
})();

var SITES = {
  generico:
    '<div class="site"><div class="nav">LOGO <i></i></div><div class="foto cinza"></div>' +
    '<h3>Bem-vindo ao nosso site</h3><p>Soluções com qualidade e excelência para você.</p><div class="lines"><i></i><i></i><i></i></div></div>',

  /* D04 · clínica odontológica fictícia */
  clinica_antes:
    '<div class="site"><div class="nav">CLÍNICA SORRIR <i></i></div><div class="foto cinza"></div>' +
    '<h3>Bem-vindo à Clínica Sorrir</h3><p>Cuidando do seu sorriso com carinho e dedicação.</p><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="lines"><i></i><i></i><i></i></div><div class="foto cinza" style="height:200px"></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="btn ghost contato">Fale conosco</div><div class="foot"><b>Clínica Sorrir</b><span>Rua Exemplo, 100</span></div></div>',
  clinica_depois:
    '<div class="site"><div class="nav">CLÍNICA SORRIR <i></i></div>' +
    '<h3>Implante dentário com avaliação em 24 horas.</h3><p>Para quem quer voltar a sorrir sem esperar meses.</p>' +
    '<div class="btn" id="wbtn">Agendar pelo WhatsApp</div><div class="foto clinica"></div></div>',

  /* D06 · estúdio fictício, bonito e decorativo */
  decorativo:
    '<div class="site"><div class="nav">ATELIÊ NORTE <i></i></div><div class="slider"><h4>Inovação que transforma.</h4><div class="dots"><i></i><i></i><i></i><i></i></div></div>' +
    '<p style="text-align:center">Excelência em cada detalhe.</p><div class="foto studio" style="height:240px"></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="foto cinza" style="height:240px"></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="foot"><b>Ateliê Norte</b><span>Rua Exemplo, 200</span><span class="contato">Contato</span></div></div>',

  /* site claro genérico de serviço (D06, D26 depois) */
  moderno:
    '<div class="site"><div class="nav">ATELIÊ NORTE <i></i></div>' +
    '<h3>Projeto de interiores para apartamentos compactos.</h3><p>Do layout à obra, com orçamento fechado.</p>' +
    '<div class="btn" id="wbtn">Pedir orçamento no WhatsApp</div><div class="foto studio"></div></div>',

  /* D26 · site antigo */
  antigo2019:
    '<div class="site velho"><div class="topo">ATELIÊ NORTE <span style="font-size:16px;font-weight:400">MENU ▾</span></div>' +
    '<div class="menu"><span>HOME</span><span>QUEM SOMOS</span><span>SERVIÇOS</span><span>GALERIA</span><span>CONTATO</span></div>' +
    '<div class="quebra">Seja bem-vindo ao site oficial do Ateliê Norte Interiores e Decorações Ltda!!</div>' +
    '<p>Somos uma empresa que atua no ramo de projetos de interiores com qualidade e excelência, buscando sempre a satisfação total de nossos clientes.</p>' +
    '<div class="banco stock"><i style="left:40px"></i><i style="left:170px;height:210px;background:#7E93A6"></i><i style="left:300px"></i><span class="marca">banco de imagem</span></div>' +
    '<p>Clique aqui para saber mais sobre nossos serviços e conhecer nossa galeria de fotos.</p>' +
    '<div class="form"><b>Fale conosco</b>Nome:<i></i>E-mail:<i></i>Mensagem:<i style="height:60px"></i><u>Enviar</u></div>' +
    '<div class="rodape">© 2019 Ateliê Norte · Todos os direitos reservados</div></div>',

  /* D11 · WhatsApp escondido x fixo */
  whats_escondido:
    '<div class="site"><div class="nav">ESTÚDIO LUME <i></i></div><h3>Fotografia de produto para lojas online.</h3><p>Fundo infinito, edição e entrega em alta resolução.</p>' +
    '<div class="foto studio"></div><div class="lines"><i></i><i></i><i></i></div><div class="foto cinza" style="height:220px"></div>' +
    '<div class="lines"><i></i><i></i><i></i></div><div class="foto cinza" style="height:220px"></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="foot"><b>Estúdio Lume</b><span>Rua Exemplo, 300</span><span class="wz">WhatsApp</span></div></div>',
  whats_fixo:
    '<div class="site"><div class="nav">ESTÚDIO LUME <i></i></div><h3>Fotografia de produto para lojas online.</h3><p>Fundo infinito, edição e entrega em alta resolução.</p>' +
    '<div class="foto studio"></div><div class="lines"><i></i><i></i><i></i></div></div><div class="sticky">Pedir orçamento no WhatsApp</div>',

  /* D14 · academia fictícia */
  academia_antes:
    '<div class="site"><div class="nav">FORMA ACADEMIA <i></i></div><div class="foto cinza"></div><h3>Supere seus limites!</h3>' +
    '<p>A melhor academia para você alcançar seus objetivos.</p><div class="lines"><i></i><i></i><i></i></div><div class="btn ghost">Saiba mais</div></div>',
  academia_depois:
    '<div class="site" style="gap:20px"><div class="nav">FORMA ACADEMIA <i></i></div><div class="faixa">Unidade Centro · 5h às 23h</div>' +
    '<h3>Treine perto de casa. A primeira aula é por nossa conta.</h3>' +
    '<div class="btn">Agendar aula experimental</div>' +
    '<div class="plano"><span>Mensal</span><b>R$ 99</b></div><div class="plano"><span>Anual · por mês</span><b>R$ 79</b></div>' +
    '<p style="font-size:19px">Sem taxa de matrícula. Cancele quando quiser.</p></div>',

  /* D23 · loja online fictícia */
  loja_antes:
    '<div class="site" style="gap:20px"><div class="nav">CASA TERRA <i></i></div><div class="foto loja"><div class="obj"></div></div>' +
    '<h3 style="font-size:44px">Vaso Cerâmica Verde</h3><div class="preco"><b>R$ 189</b></div><p class="preco-x">Frete calculado no carrinho.</p>' +
    '<div class="lines"><i></i><i></i><i></i></div><div class="lines"><i></i><i></i><i></i></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="btn comprar">Comprar</div><div class="foot"><b>Casa Terra</b><span>Loja demonstrativa</span></div></div>',
  loja_depois:
    '<div class="site" style="gap:18px"><div class="nav">CASA TERRA <i></i></div><div class="foto loja" style="height:270px"><div class="obj"></div></div>' +
    '<h3 style="font-size:44px">Vaso Cerâmica Verde</h3><div class="preco"><b>R$ 189</b><span>frete grátis acima de R$ 150</span></div>' +
    '<span class="stars">★★★★★ 4,9 · 212 avaliações</span><div class="btn comprar">Comprar agora</div>' +
    '<p style="font-size:19px">Chega em 3 a 5 dias úteis. Troca grátis em 30 dias.</p></div><div class="sticky">Comprar · R$ 189</div>',

  /* D21 · escritório de contabilidade fictício */
  texto_antes:
    '<div class="site"><div class="nav">CONTÁBIL PRIME <i></i></div><div class="foto cinza"></div>' +
    '<h3>Qualidade e excelência em contabilidade.</h3><p>Soluções completas para sua empresa, com atendimento diferenciado.</p><div class="lines"><i></i><i></i><i></i></div></div>',

  /* D16 · três sites para o teste */
  testeA:
    '<div class="site"><div class="nav">VIVA BEM <i></i></div><div class="foto cinza"></div><h3>Bem-vindo ao nosso espaço</h3>' +
    '<p>Cuidando de você com qualidade.</p><div class="lines"><i></i><i></i><i></i></div></div>',
  testeB:
    '<div class="site"><div class="nav">PÉ FIRME <i></i></div><h3>Fisioterapia para dor nas costas.</h3><p>Avaliação completa na primeira consulta.</p>' +
    '<div class="foto academia" style="height:420px"></div><div class="lines"><i></i><i></i><i></i></div><div class="lines"><i></i><i></i><i></i></div>' +
    '<div class="btn ghost">Contato</div></div>',
  testeC:
    '<div class="site"><div class="nav">PÉ FIRME <i></i></div><h3>Fisioterapia para dor nas costas, perto de você.</h3><p>Para quem trabalha sentado e quer voltar a se mexer sem dor.</p>' +
    '<div class="btn" id="wbtn">Agendar pelo WhatsApp</div><div class="foto academia"></div></div>',

  /* D19 · perfil de empresa numa busca (interface genérica) */
  perfil:
    '<div class="site" style="gap:20px"><div class="perfil-top"><span class="sel">Perfil da empresa</span><h3>Studio Forma</h3>' +
    '<span class="stars">★★★★★ 4,9 · 87 avaliações</span><span class="cat">Arquiteto de interiores</span><span class="hor">Aberto · fecha às 18h</span></div>' +
    '<div class="acoes"><span class="bsite">Site</span><span>Rotas</span><span>Ligar</span></div>' +
    '<div class="fotos"><i></i><i></i><i></i></div>' +
    '<div class="aval"><b>“Projeto entregue no prazo.”</b><span>Avaliação de exemplo</span></div><div class="lines"><i></i><i></i><i></i></div></div>'
};
