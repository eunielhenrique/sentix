# Sentix — Prompt do front (plataforma completa, por fases)

Você vai construir o **front da Sentix**, uma plataforma brasileira de vendas por telefone e WhatsApp:
discador web, kanban de leads com captura da Meta e distribuição automática, módulo de conversa de
WhatsApp, análise de ligações e chats por IA com coaching do vendedor, gamificação (pódio, medalhas,
diamantes) e agente de voz com IA. A voz roda sobre a **API4COM** (PBX SIPPulse) por baixo; no futuro,
SIPPulse próprio. Produto novo, repositório novo, sem relação com nenhum outro projeto.

**Regra de marca:** identidade própria. É proibido copiar layout, textos, ícones, cores ou nome da
API4COM ou de qualquer concorrente (Kommo, Digisac, Umbler, Huggy…). Replicamos função, não interface.

**Regra de honestidade:** dado real ou estado vazio. Mock nunca se apresenta como real. Enquanto não
existe backend para um módulo, ele roda contra uma camada de API tipada com um adaptador `local`
claramente rotulado "Dados de demonstração" no cabeçalho da tela.

---

## 1. Stack e estrutura

- React 18+ com Vite, TypeScript. React Router. Estado por Context + hooks; sem Redux.
- `jssip` para SIP/WebRTC. Tailwind ou CSS próprio com tokens (cores, espaçamento, raio, sombra) num
  único arquivo `tokens.css`. Tema claro e escuro desde o início.
- Componentes base próprios em `src/kit/`: Button, Input, Select, Card, Drawer, Modal, Tabs, Badge,
  Avatar (foto + iniciais como fallback), Table, Skeleton, Toast, Icon (um único set de ícones SVG).
- Camada de dados em `src/api/` com **interfaces** e adaptadores:
  - `voice/` → `VoiceAdapter` (interface) + `api4comAdapter` (JsSIP, real). Amanhã `sippulseAdapter`.
  - `crm/` → leads, kanban, interações, vendedores (adaptador `local` até existir backend).
  - `whatsapp/` → conexão QR, conversas, mensagens (adaptador `local` até existir o motor).
  - `insights/` → análises, coaching, gamificação (adaptador `local`).
  Nenhuma tela chama fetch direto; tudo passa pelos adaptadores.
- Layout: shell com barra lateral de módulos (desktop) e barra inferior (mobile), topo com busca,
  status do ramal, saldo, presença e avatar. **Discador é um widget flutuante global**, montado uma
  vez no shell, aberto por evento (`openDialer({ number, name, leadId })`).
- Responsivo: desktop primeiro (vendedor trabalha no computador), mobile funcional para gestor.

## 2. Módulos e telas

### 2.1 Login e conta
- Login com e-mail e senha da API4COM (`POST /users/login`) nesta fase. Logout real. Recuperar senha
  aponta para o fluxo da operadora. Token só em memória ou `sessionStorage`.
- Onboarding em 3 passos na primeira entrada: permissão de microfone, teste de áudio, conectar
  WhatsApp (pode pular).

### 2.2 Discador (widget global) — FASE 1
Funcional quando: registra o ramal; faz e recebe chamada com áudio nos dois sentidos; mudo, espera,
DTMF, transferência, desligar, cronômetro; histórico; equipe; saldo; `openDialer` abre já discando.

- Estados visíveis: conectando, online, offline, reconectando; erro humano quando o registro falha.
- Teclado, campo de número com normalização (aceita colar com máscara; envia E.164 sem "+"; se o PBX
  rejeitar, testar formato nacional e documentar no README).
- Tela de chamada: nome/foto/cidade do lead quando vier do kanban; botões Mudo, Espera, Teclado,
  Transferir (lista de ramais da equipe), Desligar; cronômetro; barra de volume.
- **Modo power (item 4 do benchmark):** botão "Próximo da fila" que disca o próximo card do vendedor
  assim que a chamada anterior é encerrada e o resultado é registrado. Preditivo NÃO.
- **Ao desligar, obrigatório registrar o resultado** numa lista fechada (item 5): Atendeu · Não atendeu ·
  Caixa postal · Número inválido · Ocupado · Recusou · Sem interesse · Recebeu material · Entrou no grupo ·
  Apoiador ativo · Agendar retorno. Caixa postal e chamada < 3 s vêm pré-selecionados quando o
  adaptador detectar; nunca contam como tentativa útil.
- Histórico (hoje/ontem/3 dias, busca), Equipe (ramais com clique para ligar), Configurações (mic,
  alto-falante, volumes, país padrão, BINA por região quando existir).
- Chamada recebida: toque, tela de atendimento com quem está ligando e vínculo ao card se o número
  existir na base.

Configuração SIP (idêntica ao webphone da operadora):
```js
new JsSIP.UA({
  sockets: [new JsSIP.WebSocketInterface(`wss://${domain}:6443`)],
  uri: `sip:${username}@${domain}`, password, realm: domain,
  register: true, register_expires: 600, no_answer_timeout: 30,
  user_agent: 'sentix-dialer/0.1',
  connection_recovery_min_interval: 2, connection_recovery_max_interval: 30,
});
```
Chamada: `ua.call(`sip:${numero}@${domain}`, { mediaConstraints: { audio: true, video: false } })`.
Eventos: `progress`, `accepted`, `confirmed`, `hold/unhold`, `muted/unmuted`, `ended`, `failed`.
Recebida: `ua.on('newRTCSession')` com `originator === 'remote'`. Transferência: `session.refer(...)`.
DTMF: `session.sendDTMF(tecla)`. Áudio remoto num `<audio autoplay>` via `session.connection.ontrack`.

Contratos da API4COM (base `https://api.api4com.com/api/v1/`, header `Authorization: <token>` sem "Bearer"):

| O quê | Chamada | Retorno |
|---|---|---|
| Login | `POST /users/login` `{ email, password }` | `{ id: token, ttl }` |
| Perfil | `GET /users/me` | `{ uuid, name, email, role }` |
| Credenciais SIP | `GET /integrations?filter[where][gateway]=sippulse` | `[{ metadata: { domain, username, password } }]` |
| Saldo | `GET /credits/balance` | `{ balance: "1138.56" }` |
| Equipe | `GET /extensions` | `[{ ramal, first_name, email_address }]` — nunca exibir/armazenar `senha` |
| Histórico | `GET /calls?page=1&filter=<JSON url-encoded>` com `{"where":{},"limit":50,"order":"started_at desc"}` | `{ data: [...] }` — documentar os campos reais |

**Teste obrigatório antes de qualquer tela:** registrar o ramal a partir de um softphone próprio, na
máquina do dev (proxies corporativos bloqueiam a porta 6443). Script em `tests/sip-register.mjs`
(Playwright + JsSIP empacotado com esbuild; credenciais por env `SIP_DOMAIN`, `SIP_USER`, `SIP_PASS`;
disca para o ramal inexistente `1999` e espera `REGISTERED` seguido de `call failed: Not Found`).
Se vier `registrationFailed 403`, testar `user_agent: 'api4com-webphone(5.12.0)'` e reportar.

### 2.3 Kanban de leads — FASE 2
Colunas fixas: **Novo → Em contato → Sem sucesso → Engajado → Encerrado**.

- Card: nome (ou telefone), cidade/DDD, avatar do vendedor (vazio se não atribuído), ícone de origem
  (Meta, importação, manual), tempo na coluna, último resultado ("Não atendeu · 3ª tentativa"),
  próximo passo agendado, botões **Ligar** e **WhatsApp**.
- Clique → **Drawer** à direita com três blocos: **Cliente** (dados e campos do formulário, editável),
  **Plataforma** (origem/campanha, entrada, coluna, histórico de movimentos, linha do tempo de
  interações: ligações com duração/resultado/gravação/transcrição, mensagens, chamadas da IA;
  tentativas; próximo passo; **consentimento**: origem do opt-in e base legal), **Vendedor** (quem,
  quando, por qual regra, tempo até o primeiro contato, botão Reatribuir para gestor). Rodapé: Ligar,
  WhatsApp, Registrar resultado, Mover para.
- Arrastar: só para a coluna **seguinte ou anterior**; soltar em coluna não adjacente devolve com
  aviso. Mover para Sem sucesso/Encerrado exige motivo da lista fechada; para Engajado exige o
  resultado positivo. Todo movimento grava quem/quando/de→para/motivo; automáticos aparecem como
  "sistema". Vendedor move só os próprios; gestor move todos.
- Topo: filtros (vendedor, origem, DDD/região, período, tentativas), busca, contadores por coluna,
  **SLA de primeiro contato** (leads sem contato há mais de N minutos em destaque).
- Importação de planilha (CSV/Google Sheets) com mapeamento de colunas e deduplicação por telefone.
- Regras de distribuição (tela do gestor): rodízio, por região (DDD), limite de cards abertos por
  vendedor, devolver à fila após N minutos sem contato, encaminhar à IA fora do horário.
- Cadência: "Não atendeu" agenda retentativa automática e oferece WhatsApp de fallback.

### 2.4 WhatsApp — FASE 3
- Conectar: modal com QR code gerado pelo motor; estados aguardando leitura / conectado /
  desconectado; botão reconectar. Estado sempre visível no topo do módulo e no card do vendedor.
- Layout do WhatsApp Web: lista de conversas (busca, filtros: não respondidas, aguardando lead, por
  coluna do kanban, etiquetas) à esquerda; conversa à direita com mídia, áudio (com transcrição),
  status de entrega.
- Funções além do WhatsApp: vínculo ao card (abrir drawer, registrar resultado sem sair), respostas
  rápidas com atalho "/", envio do material em um clique, **dois botões de IA** (Sugerir resposta e
  Otimizar meu texto; nunca um só), agendamento de mensagem, transferência de conversa, etiquetas,
  Ligar direto do chat, visão do gestor com tempo de primeira resposta.
- **Painel de saúde do número** (item 10): mensagens novas/dia, taxa de resposta, bloqueios,
  desconexões, com limite diário configurável e aviso antes de atingir.
- Opt-out em 48 h e registro de consentimento visíveis na conversa.

### 2.5 Insights e coaching — FASE 4
- Por interação (ligação ou chat): resumo, próximos passos, objeções detectadas e rubrica de 6
  critérios (abertura, escuta, objeções, clareza da proposta, fechamento, próximo passo) de 1 a 5 com
  trecho como evidência. Mesma rubrica para voz e texto.
- **Página do vendedor**: evolução dos 6 critérios por semana, 3 pontos fortes, 3 a melhorar com
  trechos reais, meta da semana, histórico de metas. Gestor vê todos; vendedor vê a própria.
- Painel do gestor: ranking por critério, comparação entre vendedores e regiões, objeções mais
  frequentes da semana.

### 2.6 Gamificação — FASE 4
- Pódio semanal e mensal (1º ao centro, maior), ranking completo com posição, variação vs. semana
  anterior e streak. Ranking por região além do geral.
- Pontos por **resultado** (engajado, entrou no grupo, apoiador ativo) e por comportamento
  (primeiro contato < 5 min, retentativa cumprida, nota de escuta ≥ 4 na semana). Nunca por volume
  de discagem. Nota da IA entra com peso menor que resultado real.
- Medalhas com critério explícito e diamantes como moeda de temporada. Perfil do vendedor com vitrine.
- Regras editáveis pelo gestor numa tela simples (o que vale ponto e quanto).

### 2.7 Agente de voz (Retell) — FASE 5
- Tela de configuração do agente (persona, roteiro, horários, quando entra: lead sem contato após N
  min, fora do horário), painel de chamadas da IA na mesma linha do tempo, transferência para humano.
- Cada chamada da IA vira interação com transcrição e análise, vendedor "IA".

### 2.8 Painel de gestão (administração) — entregue junto com a FASE 1 no que depende só da operadora
Nove telas, especificadas em `docs/PORTAL_TELAS.md` (função replicada, layout próprio):

1. **Dashboard**: filtros (usuários, período, sentido, status), cartões (total de chamadas, atendidas,
   ramais, taxa de atendimento, tempo falado, TMA + leads novos, tempo até 1º contato, conversas,
   engajados), tabela de desempenho por usuário (taxa de atendimento, canceladas, espera antes de
   desligar, rediscagens, chamadas significativas, a cada 100 ligações + leads, engajados, nota da IA,
   pontos), gráfico de chamadas por usuário no tempo e rosca por status.
2. **Relatórios**: Chamadas / Usuários / Conversas / Leads; filtros em pills com chips removíveis;
   tabela de chamadas com data, usuário, número, duração, motivo do desligamento, tipo, ramal, fim,
   tarifa, custo, metadados (drawer), gravação (player) + lead vinculado, resultado, nota, transcrição;
   exportar CSV.
3. **Assinatura e uso**: consumo por usuário no mês, plano sugerido, resumo da cobrança.
4. **Usuários**: total ativos, busca, filtro de status, convidar (nome, e-mail, papel, equipe/região,
   ramal), tabela com ramal, equipe, papel, status, WhatsApp conectado, ações. Um ramal por usuário ativo.
5. **Integrações**: abas CRM / Ramal / Webhook + Meta / WhatsApp / Operadora / IA / Agente de voz.
6. **Tokens de acesso**: criar (nome, validade, escopo), listar mascarado, copiar, remover, último uso.
7. **Recarga e créditos**: valor com régua de desconto por faixa que recalcula minuto móvel/fixo,
   e-mails do financeiro, prazos por meio de pagamento; lê saldo e tarifa da operadora.
8. **Menu da conta**: meus dados, alterar senha, acesso do suporte (personificação autorizada e
   auditada), histórico de cobranças, recarga automática, dados financeiros, dados da organização, sair.
9. **Topo**: saldo disponível com botão de recarga; status do ramal; presença; avatar.

Na fase 1, Dashboard, Relatórios, Usuários, Tokens, Recarga e Menu da conta já funcionam com dado
real da API4COM (adaptador de voz + `/users`, `/extensions`, `/calls`, `/credits/balance`,
`/charges?page=1`, `/users/accessTokens`). Assinatura e Integrações nascem com adaptador `local`.

## 3. Padrões de interface (valem em toda tela)

- Skeleton enquanto carrega; passado o tempo sem dado → estado vazio honesto. Nunca "0" sobre fetch.
- Delta sempre com sinal e cor pelo sinal. Indicadores visuais com ícone do kit, nunca emoji.
- Toda pessoa com Avatar (foto, iniciais como fallback). Toda lista longa com scroll infinito.
- Drawer e Modal são peças únicas do kit, chamadas na raiz da tela, nunca dentro de card.
- Ações destrutivas pedem confirmação. Erros de API viram mensagem humana com o que fazer.
- Acessível: foco visível, navegação por teclado no discador e no kanban, contraste AA.
- Português do Brasil em toda a interface; textos centralizados em um arquivo de mensagens.

## 4. Segurança

- Token e senha SIP só em memória/`sessionStorage`; nunca `localStorage`, cookie, URL ou log.
- Nenhuma credencial no repositório; testes leem env. Sem log de payload em produção.
- O front nunca fala com o motor de WhatsApp nem com a Retell diretamente; sempre via adaptador
  (que hoje aponta para `local` e amanhã para o backend).

## 5. Ordem de entrega e aceite

| Fase | Entrega | Aceite |
|---|---|---|
| 1 | Shell, login, kit base, **discador completo** (2.2) | Teste SIP passou (log no PR sem senha); chamada real com áudio nos dois sentidos; recebida toca; resultado obrigatório ao desligar; `openDialer` funciona |
| 2 | Kanban + drawer + importação + regras de distribuição (2.3) com adaptador `local` | Arrastar só adjacente; motivos obrigatórios; histórico de movimentos; card → Ligar abre o discador com o número |
| 3 | WhatsApp (2.4) com adaptador `local` e contrato do motor documentado | QR → estados; chat completo; dois botões de IA; painel de saúde |
| 4 | Insights, coaching e gamificação (2.5, 2.6) | Rubrica por interação; página do vendedor; pódio e ranking com regras editáveis |
| 5 | Agente de voz (2.7) e administração completa (2.8) | Configuração do agente; chamadas da IA na linha do tempo |

Uma feature por branch → PR. No PR: checklist da fase, o que divergiu desta spec, campos reais das
APIs descobertos. Se um contrato estiver ambíguo, anote no PR e não invente campo. Reporte por item.
