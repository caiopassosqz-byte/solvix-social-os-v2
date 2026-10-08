# Integração com o Instagram da Solvix

Como os posts aprovados no painel são publicados automaticamente.

## Como funciona agora: API da Meta (ativo desde 08/10)

1. Você aprova o post no painel (ou pede ajuste). Só sai o que estiver **Aprovado**.
2. Nos horários da agenda (Estratégia › Horários), uma rotina do Claude roda `publicar/publicar.py devidos`, que publica no @solvixagencybr o post do dia e os Stories daquele horário pela API oficial da Meta.
3. Cada publicação fica anotada em `publicar/registro.json`, e o post muda para **Publicado** no painel, com o link.

Horários das rotinas (Brasília): seg a sex 12:30, 19:00, 19:20 e 21:00; sáb, dom e feriado 09:30, 11:00, 11:20 e 20:00. Feriados do ciclo (em `painel/plano.json`, agenda.feriados): 12/10 e 02/11, com rotinas avulsas nesses dias.

Como a conta está ligada:
- Página Solvix Agency e @solvixagencybr pertencem ao portfólio "Solvix Agency | Desenvolvimento Web" e estão compartilhados como parceiro com o portfólio "Solvix Agency" do Caio (ID 1966517390683663).
- O app "Solvix Publicador." (ID 2164053351161557) pertence ao portfólio do Caio. O usuário do sistema **publicador** gera o token, que não expira.
- O token fica só no segredo `META_TOKEN` do ambiente, liberado apenas para graph.facebook.com. Nunca no chat nem no repositório.
- As mídias são lidas pela Meta do repositório público (raw.githubusercontent.com). Imagens vão em JPEG (`publicar/jpg/`, gerado por `python3 publicar/publicar.py jpg`).

Comandos úteis: `python3 publicar/publicar.py agenda` (o que sai e quando) e `python3 publicar/publicar.py testar D05-post` (cria a mídia na Meta sem publicar).

Não agende os mesmos posts no Meta Business Suite: eles sairiam duas vezes.

## Caminho antigo: Meta Business Suite + Claude no navegador

1. Crie a página do Facebook "Solvix Agency" (categoria Web Designer) e ligue ao @solvixagencybr. O Business Suite precisa dela.
2. Aprove os posts no painel.
3. No Chrome, logado no Facebook, abra o painel na aba **Agendar**, clique em **Copiar roteiro** e cole no Claude do navegador.
4. Ele agenda no business.facebook.com só o que estiver aprovado (post, legenda, horário e Stories) e marca cada item como Agendado no painel. Se a janela de arquivos do computador travar, ele pede para você escolher o arquivo.

## Caminho pago: Postiz



O Claude não entra no Instagram com login e senha. A publicação passa pelo **Postiz**, uma ferramenta de agendamento que usa a API oficial da Meta. Você conecta o Instagram no Postiz uma vez; depois o Claude envia cada post aprovado (mídia, legenda, data e hora) para o Postiz, que publica no horário.

Só vai para o Postiz o que estiver **Aprovado** no painel. Nada é publicado sem a sua aprovação.

## O que você faz (uma vez só)

1. **Conta profissional no Instagram.** No app: Configurações › Tipo de conta › Mudar para conta profissional (Empresa).
2. **Facebook é opcional.** O Postiz tem duas formas de conectar: "Instagram (Standalone)", que entra direto com o login do Instagram, sem Facebook, e "Instagram (Facebook Business)", que precisa de uma página do Facebook ligada à conta. Use a Standalone. A única diferença é que ela não escolhe música da biblioteca do Instagram para o Reels; os nossos Reels já têm a trilha dentro do vídeo, então não muda nada.
3. **Conta no Postiz.** Crie em postiz.com e adicione o canal "Instagram (Standalone)". Entre com o login do @solvixagencybr e autorize.
4. **Chave da API.** No Postiz: Settings › Public API › gere a chave.
5. **Guarde a chave no ambiente do Claude, não no chat.** No menu do ambiente na barra de título da sessão, clique em Edit e adicione a chave em *Network secrets* (ou como variável de ambiente) com o nome `POSTIZ_API_KEY`.
6. **Libere o endereço do Postiz.** Na mesma tela, em *Network access*, adicione `api.postiz.com` em *Allowed domains* (deixe marcada a opção de gerenciadores de pacote). Hoje esse endereço está bloqueado pela política de rede do ambiente. Passo a passo: https://code.claude.com/docs/en/cloud-environments#network-access
7. **Abra uma sessão nova** e me avise. A chave e a liberação só valem para sessões abertas depois da mudança.

Nunca cole a chave, senha ou código de acesso no chat.

## Links do perfil (você coloca no app)

Editar perfil › Links › Adicionar link externo:

1. **WhatsApp:** https://wa.me/5599981726563?text=Oi!%20Vim%20pelo%20Instagram%20da%20Solvix. (título: Falar no WhatsApp)
2. **Site:** https://solvixagency.vercel.app (título: Ver projetos)

## O que o Claude faz depois

1. Confere a conexão: lista os canais do Postiz e as configurações exigidas pelo Instagram.
2. Para cada post **Aprovado** no painel: envia a mídia (vídeo do Reels ou slides do carrossel), a legenda da pasta do post e agenda no dia do calendário, no horário da agenda (Estratégia › Horários: 19h nos dias úteis, 11h no fim de semana). Os Stories do dia (pasta `stories/dNN/`) vão junto: o bastidor no almoço, o story do post 20 minutos depois dele e a palavra-chave às 21h.
   - A API do Instagram publica Stories como imagem, sem adesivos. A pergunta da manhã já pede resposta na própria arte. Se quiser a enquete clicável, poste esse Story pelo app e ponha o adesivo no espaço livre abaixo da pergunta.
3. Marca o post como **Agendado** no painel e, depois de publicado, como **Publicado**.
4. Se algo falhar (mídia recusada, conta desconectada), o post volta para **Aprovado** com a nota do erro, e você é avisado.

## Antes do primeiro agendamento

Pendências que travam posts específicos (também aparecem no painel, em Hoje):

| Pendência | Posts |
|---|---|
| Números reais do Insights | D13, D30 |
| Confirmar domínio no nome do cliente e suporte depois da entrega (contrato e 50% + 50% já confirmados) | D17, D18, D29 e guia de investimento |
| Revisar os materiais das palavras-chave | D05, D10, D24 |
| Limite semanal e prazo da análise gratuita | D24 |
