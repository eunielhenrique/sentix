# Sentix — Módulo WhatsApp (especificação, decisão do Euniel em 22/09/2026)

## Decisão

Cada vendedor conecta o **próprio número** lendo um **QR code** gerado pela Sentix. Depois de
conectado, a Sentix abre um **módulo de conversação** com a experiência do WhatsApp e funções a mais.
Isso implica usar o protocolo do WhatsApp Web (via um motor como Evolution API, Baileys ou
WPPConnect), e não a API oficial da Meta. Os dois caminhos ficam previstos na arquitetura.

## Riscos aceitos do caminho por QR (registrar para o cliente saber)

- É uso fora dos termos da Meta. Números podem ser **bloqueados**, sobretudo com volume de
  mensagens iguais para muitos contatos ou muitos contatos novos por dia.
- A conexão cai quando o celular fica sem internet por muito tempo ou o WhatsApp atualiza o
  protocolo; precisa de reconexão automática e de aviso ao vendedor.
- Sem recursos oficiais: templates aprovados, botões interativos e selo verificado.

Mitigações obrigatórias: limite de mensagens novas por número por dia, intervalo aleatório entre
envios em massa, número "aquecido" antes de operar, e alerta de desconexão no card do vendedor.
A API oficial (Cloud API) fica como opção por organização para quem preferir número da empresa.

## Arquitetura

- **Motor de conexão** self-hosted (Evolution API é a opção mais madura hoje): uma instância por
  vendedor, criada pela Sentix ao clicar em "Conectar WhatsApp".
- **QR code** vem do motor e é exibido no modal; a Sentix acompanha o estado (aguardando leitura,
  conectado, desconectado) por webhook.
- **Webhooks** do motor → backend da Sentix: mensagem recebida, mensagem enviada, status de
  entrega/leitura, conexão. Tudo gravado na tabela única de **interações** (mesma da telefonia).
- Envio: backend da Sentix → motor. O front nunca fala com o motor direto.
- Mídia (áudio, imagem, documento) baixada pelo backend e guardada em storage próprio; áudio
  de WhatsApp passa pela mesma transcrição das ligações.

## Módulo de conversação

Estrutura em duas colunas, igual ao WhatsApp Web: lista de conversas à esquerda, conversa aberta
à direita. Funções além do WhatsApp:

- **Vínculo com o lead**: cada conversa aponta para o card do kanban; botão para abrir o drawer
  do lead e para registrar resultado sem sair do chat.
- **Respostas rápidas** por organização (atalho "/") e **envio do material** da campanha em um clique.
- **Sugestão de resposta pela IA** e **otimização do texto** que o vendedor escreveu (dois botões,
  nunca um só).
- **Agendamento de mensagem** e lembrete de follow-up ligado à cadência do kanban.
- **Transferência de conversa** para outro vendedor, com histórico junto.
- **Etiquetas** e filtros: não respondidas, aguardando lead, por etapa do kanban.
- **Ligar** direto do chat pelo discador.
- **Análise da IA** por conversa (mesma rubrica das ligações) alimentando coaching e gamificação.
- Visão de **gestor**: todas as conversas da equipe, tempo de primeira resposta, SLA.

## Regras

- Mensagem nunca sai sem um vendedor ou automação identificados como autor.
- Conversa e ligação do mesmo lead aparecem na mesma linha do tempo do drawer.
- Estado da conexão sempre visível no cabeçalho do módulo e no card do vendedor.
