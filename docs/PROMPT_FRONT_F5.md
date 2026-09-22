# Sentix — Prompt do front · FASE 5: Agente de voz com IA (Retell) + administração completa

## Contexto (leia antes de tudo)

A **Sentix** é uma plataforma brasileira de vendas por telefone e WhatsApp. Já existem: shell, login,
kit, discador global, painel de gestão, kanban com drawer e linha do tempo, importação, módulo de
WhatsApp, análise de IA com coaching e gamificação. Esta fase fecha o produto com o **agente de voz com
IA** (Retell por baixo, usando o tronco SIP da operadora) e a **administração completa** (assinatura e
cobrança da Sentix, integrações, consentimento e avisos legais, acesso do suporte).

Regras permanentes do projeto:
- **Marca própria.** Nada copiado de Retell, API4COM ou concorrentes.
- **Dado real ou estado vazio.** Sem backend, os módulos rodam contra adaptadores `local`
  (`src/api/voiceAgent/localAdapter.ts`, `src/api/admin/localAdapter.ts`) com selo "Dados de demonstração".
- **O front nunca fala com a Retell nem com a operadora direto.** Sempre via adaptadores; o real
  apontará para o backend da Sentix.
- **Stack e kit:** React 18+ com Vite e TypeScript, React Router, Context + hooks, tokens em
  `tokens.css` (claro/escuro), kit próprio em `src/kit/`.
- **Padrões:** skeleton e estado vazio honesto; ícones do kit; Drawer e Modal na raiz; acessível por
  teclado; erro humano com o que fazer.
- **Segurança:** chaves de integração nunca aparecem inteiras depois de salvas (mascaradas, com
  "substituir"); token só em memória/`sessionStorage`.
- Uma feature por branch → PR com checklist, divergências e campos reais.

## 1. Agente de voz com IA

### 1.1 Modelo (`src/api/voiceAgent/types.ts`)
```ts
interface AgenteVoz { id: string; nome: string; ativo: boolean; voz: { id: string; nome: string; idioma: 'pt-BR' };
  persona: string; roteiro: { abertura: string; objetivo: 'primeiro_contato' | 'qualificar' | 'agendar' | 'confirmar';
    perguntas: { chave: string; texto: string; tipo: 'texto' | 'sim_nao' | 'opcoes'; opcoes?: string[] }[];
    encerramento: string }; regras: { identificarComoIA: true; horario: { inicio: string; fim: string; dias: number[] };
    maxTentativasPorLead: number; transferirParaHumano: 'sempre_que_pedir' | 'quando_qualificado' | 'nunca';
    numeroSaida?: string /* BINA */ }; gatilhos: { leadSemContatoApos?: number /* min */; foraDoHorario: boolean;
    etapas: string[]; regioes: string[] }; custoEstimadoMin: number }
interface ChamadaIA { id: string; agenteId: string; leadId: string; inicio: string; fim?: string; duracaoSeg?: number;
  status: 'agendada' | 'discando' | 'em_andamento' | 'concluida' | 'nao_atendida' | 'falhou' | 'transferida';
  resultado?: string; respostas?: Record<string, string>; transcricao?: string; gravacaoUrl?: string;
  analise?: { resumo: string; qualificado: boolean; proximoPasso?: string; sentimento: 'positivo' | 'neutro' | 'negativo' };
  custo?: number; transferidaPara?: string }
```
Interface `VoiceAgentAdapter`: `listarAgentes()`, `salvarAgente(a)`, `testarAgente(agenteId, numero)`,
`listarChamadas(filtros, pagina)`, `obterChamada(id)`, `agendarChamada(leadId, agenteId, em?)`,
`cancelarChamada(id)`, `vozes()`, `custoEstimado(agenteId)`, `assinar('chamada.ia.atualizada', cb)`.

### 1.2 Telas
- **Agentes (`/agente-ia`)**: lista de agentes com estado, chamadas hoje, taxa de atendimento,
  custo do mês; botão Novo agente.
- **Editor do agente (`/agente-ia/:id`)** em abas:
  - *Persona e voz*: nome, voz (lista com player de amostra em pt-BR), persona (textarea com
    exemplos), aviso fixo "O agente sempre se identifica como assistente virtual" (não desativável).
  - *Roteiro*: abertura, objetivo, perguntas (lista ordenável com tipo e opções), encerramento;
    pré-visualização em formato de diálogo.
  - *Regras*: horário por dia, máximo de tentativas por lead, quando transferir para humano, número
    de saída (BINA) entre os disponíveis.
  - *Gatilhos*: lead sem contato humano após N minutos, fora do horário da equipe, etapas e regiões
    elegíveis; prévia "Ontem, com estes gatilhos, o agente teria ligado para N leads".
  - *Testar*: campo de número e botão "Ligar para mim agora" (`testarAgente`); resultado aparece em
    tempo real com transcrição.
  - Rodapé: custo estimado por minuto e por chamada média, salvar, ativar/desativar.
- **Chamadas da IA (`/agente-ia/chamadas`)**: tabela com data, agente, lead (link para o drawer),
  duração, status, resultado, qualificado (sim/não), custo, gravação (player), transcrição (drawer
  com marcação IA/lead), transferida para. Filtros por agente, status, período, região. Exportar CSV.
- **No kanban e no drawer do lead**: chamada da IA aparece na linha do tempo como interação com
  autor "IA", com resumo, respostas coletadas e botão "Assumir lead" que atribui ao vendedor e abre
  o discador. Botão **"Enviar para a IA"** no card/drawer (gestor) agenda uma chamada.
- **Distribuição (já existe)**: a opção "fora do horário → IA" e "sem contato após N min → IA" passam
  a funcionar chamando `agendarChamada`.
- **Gamificação e coaching (já existem)**: chamadas da IA entram no placar como vendedor "IA" em
  linha separada (não compete no pódio) e no painel do gestor como comparação IA × humano
  (taxa de atendimento, qualificação, custo por lead qualificado).

## 2. Administração completa

### 2.1 Assinatura e cobrança da Sentix (`/configuracoes/assinatura`)
Planos por assento (**Conversas** · **Completo** · **Pro**) com tabela de recursos, preço mensal e
anual, seleção de plano por usuário com "Aplicar a todos", resumo da cobrança (plano × quantidade,
adicionais: minutos excedentes, minutos de agente de voz, templates de WhatsApp oficial), vencimento e
próximas cobranças, método de pagamento (cartão/PIX/boleto), histórico de faturas (data, valor,
status, nota fiscal, link). Tela de **uso** do mês: minutos por usuário, chamadas da IA, mensagens,
análises de IA, com projeção do fechamento. Enquanto a operadora for a API4COM, a aba **Créditos da
operadora** mostra saldo, tarifas e recarga (tela já existente da fase 1).

### 2.2 Integrações (`/configuracoes/integracoes`)
Abas com cards de estado (Conectado/Desconectado, última sincronização, erro humano):
- **Operadora de voz**: API4COM ou SIPPulse; domínio, credenciais mascaradas, saldo, teste de registro.
- **Meta**: conectar conta (fluxo OAuth via backend), páginas, contas de anúncio, formulários de Lead
  Ads (lista com último lead recebido), número de WhatsApp da campanha.
- **WhatsApp**: modo por organização (QR por vendedor ou API oficial), status por vendedor, limites.
- **IA**: modelo de transcrição e de análise (lista fornecida pelo backend), limite de custo mensal com
  alerta, rubrica (pesos por critério editáveis), idioma.
- **Agente de voz**: chave da Retell mascarada, tronco SIP, números de saída, custo por minuto.
- **Webhooks de saída**: URL, eventos (lead.novo, lead.movido, chamada.encerrada, conversa.nova,
  analise.pronta), segredo, testar envio, histórico de entregas com reenvio.
- **CRM externos** (sob demanda): Pipedrive, HubSpot, RD Station, Kommo — cards "Solicitar".

### 2.3 Consentimento e avisos legais (`/configuracoes/consentimento`)
Texto do aviso de gravação (lido/mostrado no início da chamada; opção de tocar áudio automático),
base legal padrão por canal, texto de opt-out do WhatsApp e palavras-chave, política de retenção de
gravações e transcrições (dias), exportação de dados de um lead (LGPD) e exclusão com confirmação
dupla. Registro de quem alterou e quando.

### 2.4 Acesso do suporte (`/configuracoes/acesso-suporte`)
O cliente autoriza a equipe da Sentix a entrar na conta por tempo limitado (1 h, 24 h, 7 dias), com
motivo; vê sessões ativas e histórico auditado (quem, quando, o que abriu). Encerrar acesso a qualquer
momento. Banner visível no topo enquanto um acesso de suporte estiver ativo.

### 2.5 Organização, equipes e regiões (`/configuracoes/organizacao`)
Dados da organização (nome, logo, telefone, horário de funcionamento), equipes (nome, gestor,
membros), regiões (nome + lista de DDDs) usadas pela distribuição e pelo placar, materiais da
campanha, respostas rápidas e etiquetas (já existentes, agrupadas aqui).

### 2.6 Programa de indicação (`/indique`)
Link único por organização, créditos por indicação convertida, status das indicações. Regras em texto.

## 3. Critérios de aceite (checklist do PR)

- [ ] Editor do agente com as cinco abas, prévia do roteiro, teste real por telefone e custo estimado.
- [ ] Chamadas da IA em tabela com gravação/transcrição e na linha do tempo do lead com "Assumir lead".
- [ ] Gatilhos da distribuição acionando a IA; comparação IA × humano no painel do gestor.
- [ ] Assinatura da Sentix com planos por usuário, uso do mês e faturas; aba de créditos da operadora.
- [ ] Integrações com estado, chaves mascaradas e testes; webhooks de saída com histórico.
- [ ] Consentimento e avisos legais editáveis, retenção, exportação e exclusão de lead.
- [ ] Acesso do suporte com prazo, auditoria e banner.
- [ ] Organização, equipes, regiões e programa de indicação.
- [ ] Selo "Dados de demonstração" onde o adaptador for `local`; README com os contratos do
      `VoiceAgentAdapter` e do `AdminAdapter` para o backend implementar.
