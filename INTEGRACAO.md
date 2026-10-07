# Integração com o Instagram da Solvix

Como os posts aprovados no painel passam a ser agendados e publicados automaticamente.

## Como funciona

O Claude não entra no Instagram com login e senha. A publicação passa pelo **Postiz**, uma ferramenta de agendamento que usa a API oficial da Meta. Você conecta o Instagram no Postiz uma vez; depois o Claude envia cada post aprovado (mídia, legenda, data e hora) para o Postiz, que publica no horário.

Só vai para o Postiz o que estiver **Aprovado** no painel. Nada é publicado sem a sua aprovação.

## O que você faz (uma vez só)

1. **Conta profissional no Instagram.** No app: Configurações › Tipo de conta › Mudar para conta profissional (Empresa).
2. **Página do Facebook ligada.** A Meta exige uma página do Facebook vinculada à conta profissional do Instagram (Central de Contas › Contas › Adicionar contas).
3. **Conta no Postiz.** Crie em postiz.com e conecte o canal "Instagram (Facebook Business)". Entre com o Facebook que administra a página e autorize o Instagram da Solvix.
4. **Chave da API.** No Postiz: Settings › Public API › gere a chave.
5. **Guarde a chave no ambiente do Claude, não no chat.** No menu do ambiente na barra de título da sessão, clique em Edit e adicione a chave em *Network secrets* (ou como variável de ambiente) com o nome `POSTIZ_API_KEY`.
6. **Libere o endereço do Postiz.** Na mesma tela, em *Network access*, adicione `api.postiz.com` em *Allowed domains* (deixe marcada a opção de gerenciadores de pacote). Hoje esse endereço está bloqueado pela política de rede do ambiente. Passo a passo: https://code.claude.com/docs/en/cloud-environments#network-access
7. **Abra uma sessão nova** e me avise. A chave e a liberação só valem para sessões abertas depois da mudança.

Nunca cole a chave, senha ou código de acesso no chat.

## O que o Claude faz depois

1. Confere a conexão: lista os canais do Postiz e as configurações exigidas pelo Instagram.
2. Para cada post **Aprovado** no painel: envia a mídia (vídeo do Reels ou slides do carrossel), a legenda da pasta do post e agenda no dia do calendário, no horário definido em Estratégia › Ajustes do ciclo.
3. Marca o post como **Agendado** no painel e, depois de publicado, como **Publicado**.
4. Se algo falhar (mídia recusada, conta desconectada), o post volta para **Aprovado** com a nota do erro, e você é avisado.

## Antes do primeiro agendamento

Pendências que travam posts específicos (também aparecem no painel, em Hoje):

| Pendência | Posts |
|---|---|
| Horário de publicação | todos |
| @ da agência e link da bio | todos os que citam "link da bio" |
| Autorização do Grupo Kaza | D12 |
| Gravação com rosto e voz | D03 |
| Números reais do Insights | D13, D30 |
| Confirmar políticas (domínio, contrato, pagamento em etapas, acessos, suporte) | D17, D29 e guia de investimento |
| Revisar os materiais das palavras-chave | D05, D10, D24 |
| Limite semanal e prazo da análise gratuita | D24 |
