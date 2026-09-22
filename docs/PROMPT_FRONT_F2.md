# Sentix — Prompt do front · FASE 2: Kanban de leads + entrada de leads

## Contexto (leia antes de tudo)

A **Sentix** é uma plataforma brasileira de vendas por telefone e WhatsApp. A fase 1 entregou o shell,
o login, o kit de componentes, o discador (widget global com `openDialer({ number, name, leadId })`) e
o painel de gestão básico. Esta fase entrega o **coração do produto: o kanban de leads e a entrada
automática de leads**. A voz roda sobre a API4COM por baixo; leads chegam pelo WhatsApp (anúncios de
"Conversas no WhatsApp" da Meta), por importação de planilha e, depois, por Lead Ads.

Regras permanentes do projeto:
- **Marca própria.** Proibido copiar layout, textos, ícones ou cores de API4COM, Kommo, Digisac,
  Umbler, Huggy ou qualquer concorrente. Replicamos função, não interface.
- **Dado real ou estado vazio.** Enquanto não existe backend para um módulo, ele roda contra um
  adaptador `local` (`src/api/crm/localAdapter.ts`) que persiste em IndexedDB e mostra o selo
  "Dados de demonstração" no cabeçalho da tela. Mock nunca se apresenta como real.
- **Nenhuma tela chama fetch direto.** Tudo passa por interfaces em `src/api/*` com adaptadores.
- **Stack:** React 18+ com Vite e TypeScript, React Router, Context + hooks, Tailwind ou CSS com
  tokens em `tokens.css` (tema claro e escuro), kit próprio em `src/kit/` (Button, Input, Select,
  Card, Drawer, Modal, Tabs, Badge, Avatar com iniciais, Table, Skeleton, Toast, Icon SVG único).
- **Padrões de interface:** skeleton enquanto carrega e estado vazio honesto depois; delta com sinal
  e cor pelo sinal; ícone do kit, nunca emoji; Drawer e Modal chamados na raiz da tela; scroll
  infinito em lista longa; erro de API vira mensagem humana com o que fazer; acessível por teclado.
- **Segurança:** token só em memória/`sessionStorage`; nada de credencial no repositório.
- Uma feature por branch → PR com checklist de aceite, divergências da spec e campos reais descobertos.

## 1. Modelo de dados (tipos em `src/api/crm/types.ts`)

```ts
type Etapa = 'novo' | 'em_contato' | 'sem_sucesso' | 'engajado' | 'encerrado';
type Canal = 'whatsapp' | 'lead_ads' | 'importacao' | 'manual' | 'ligacao';
type Resultado =
  | 'atendeu' | 'nao_atendeu' | 'caixa_postal' | 'numero_invalido' | 'ocupado'
  | 'recusou' | 'sem_interesse' | 'recebeu_material' | 'entrou_no_grupo'
  | 'apoiador_ativo' | 'agendar_retorno';

interface Lead {
  id: string; telefone: string /* E.164 sem "+" */; nome?: string; cidade?: string; ddd: string;
  etapa: Etapa; vendedorId?: string; origem: { canal: Canal; plataforma?: 'meta'; contaAnuncio?: string;
    campanha?: string; anuncio?: string; ctwaClid?: string };
  consentimento: { tipo: 'mensagem_espontanea' | 'formulario' | 'importacao'; data: string; evidencia?: string };
  tentativas: number; ultimoResultado?: Resultado; proximoPasso?: { tipo: 'ligar' | 'whatsapp'; em: string };
  tags: string[]; observacoes?: string; camposFormulario?: Record<string, string>;
  criadoEm: string; atualizadoEm: string; entrouNaEtapaEm: string;
}
interface Interacao { id: string; leadId: string; tipo: 'ligacao' | 'whatsapp' | 'ia_voz' | 'nota';
  autor: { tipo: 'vendedor' | 'ia' | 'sistema'; id?: string }; inicio: string; fim?: string;
  duracaoSeg?: number; resultado?: Resultado; gravacaoUrl?: string; transcricao?: string;
  texto?: string; metadados?: Record<string, unknown> }
interface Movimento { id: string; leadId: string; de: Etapa; para: Etapa; por: { tipo: 'vendedor' | 'gestor' | 'sistema'; id?: string };
  motivo?: Resultado | string; em: string }
interface Vendedor { id: string; nome: string; email: string; avatarUrl?: string; ramal?: string;
  equipe?: string; regioes: string[] /* DDDs */; ativo: boolean; limiteCardsAbertos: number }
interface RegraDistribuicao { modo: 'rodizio' | 'regiao' | 'manual'; limitePorVendedor: number;
  devolverAposMin: number; foraDoHorarioPara: 'fila' | 'ia'; horario: { inicio: string; fim: string; dias: number[] } }
```

Interface `CrmAdapter` (todas assíncronas): `listarLeads(filtros, pagina)`, `obterLead(id)`,
`criarLead(input)`, `atualizarLead(id, patch)`, `moverLead(id, para, motivo?)`, `registrarResultado(leadId,
resultado, nota?)`, `atribuir(leadId, vendedorId, regra)`, `listarInteracoes(leadId)`, `listarMovimentos(leadId)`,
`importar(linhas, mapeamento)`, `listarVendedores()`, `obterRegras()`, `salvarRegras(r)`, `contadoresPorEtapa(filtros)`,
`assinar(evento, cb)` para `lead.novo`, `lead.movido`, `lead.atribuido`. O adaptador `local` implementa
tudo, inclusive o rodízio e a devolução à fila por tempo (timer no cliente, marcado como "sistema").

## 2. Tela Kanban (`/leads`)

Colunas fixas na ordem **Novo → Em contato → Sem sucesso → Engajado → Encerrado**, com contador e
soma de leads sem contato há mais de N minutos (SLA) em destaque no cabeçalho da coluna Novo.

Topo: busca (nome/telefone), filtros em pills (vendedor, origem, DDD/região, período de entrada,
tentativas, só meus), chips removíveis dos filtros ativos, botões **Importar** e **Novo lead**
(manual), seletor "Cards compactos / detalhados".

**Card:** nome (ou telefone formatado quando não há nome) · cidade/DDD · avatar do vendedor (vazio
com contorno tracejado se não atribuído) · ícone da origem (Meta, planilha, manual) · tempo na coluna
(relativo: "há 12 min") · último resultado com tentativa ("Não atendeu · 3ª") · próximo passo agendado
· botões rápidos **Ligar** (chama `openDialer` com número, nome e leadId) e **WhatsApp** (abre a
conversa; na fase 2, `wa.me` com o número até o módulo de chat existir). Card com SLA estourado ganha
borda de alerta.

**Arrastar e soltar** (biblioteca: `@dnd-kit/core`, acessível por teclado):
- Só para a coluna **seguinte ou anterior**. Soltar em coluna não adjacente devolve o card ao lugar
  com toast "Mova uma etapa por vez".
- Para **Sem sucesso** ou **Encerrado**: modal obrigatório com o motivo (lista fechada `Resultado` +
  campo livre opcional). Cancelar devolve o card.
- Para **Engajado**: modal com o resultado positivo (recebeu material, entrou no grupo, apoiador ativo).
- Todo movimento grava `Movimento` (quem, quando, de → para, motivo). Vendedor move só os próprios
  cards; gestor move todos. Movimentos automáticos aparecem como "sistema".
- Feedback otimista com rollback se o adaptador falhar.

## 3. Drawer do lead (abre ao clicar no card; `Drawer` do kit na raiz da tela; largura 520)

Cabeçalho: nome ou telefone, etapa (badge), vendedor, botões Ligar e WhatsApp. Três blocos em abas
ou seções empilhadas:

1. **Cliente** — telefone(s), nome, cidade, DDD/região, campos do formulário (quando Lead Ads), tags
   (chips editáveis), observações (textarea com autosave). Tudo editável inline.
2. **Plataforma** — origem (canal, campanha, anúncio, com ícone), data de entrada, etapa atual e tempo
   nela, **histórico de movimentos** (lista: data, de → para, quem, motivo), **linha do tempo de
   interações** (ligações com duração/resultado/link da gravação/transcrição quando houver, mensagens
   de WhatsApp, chamadas da IA, notas), contador de tentativas, próximo passo (editar/agendar),
   **consentimento** (tipo, data, evidência: primeira mensagem ou formulário).
3. **Vendedor** — quem recebeu, quando, por qual regra (rodízio/região/manual), tempo até o primeiro
   contato, botão **Reatribuir** (só gestor: select de vendedor + motivo).

Rodapé fixo: **Ligar** · **WhatsApp** · **Registrar resultado** (abre o mesmo modal de resultado do
discador; grava `Interacao` tipo nota/ligação e move o card pelas regras) · **Mover para** (menu com
apenas a etapa anterior e a seguinte).

## 4. Entrada de leads

### 4.1 Importação de planilha (`/leads/importar`)
Wizard em 3 passos: (1) upload CSV/XLSX ou colar link público do Google Sheets; (2) mapeamento de
colunas (Nome, Telefone, Cidade, Feedback → resultado inicial, Observação) com pré-visualização das
10 primeiras linhas e **mapa texto → resultado** editável (ex.: "Não atendeu" → `nao_atendeu`,
"Caixa postal"/"Cx Postal" → `caixa_postal`, "apoiando/divulga/grupo" → `apoiador_ativo`, vazio → sem
contato); (3) resumo: novos, duplicados por telefone (ignorados ou atualizados), inválidos, e botão
Importar. Cada linha vira `Lead` com `origem.canal = 'importacao'`, `consentimento.tipo = 'importacao'`,
etapa derivada do resultado (sem contato → Novo; tentativa sem sucesso → Sem sucesso; positivo →
Engajado; recusa → Encerrado). Relatório final exportável.

### 4.2 Conexão de WhatsApp por QR e criação automática de card
Tela `/whatsapp/conectar` (por vendedor): botão **Conectar meu WhatsApp** abre modal com o QR code
vindo do adaptador `whatsapp` (`obterQr()`, `estado()`: aguardando_leitura | conectado | desconectado
| reconectando), instruções em 3 passos, estado em tempo real e botão Reconectar. Estado da conexão
visível no topo do shell e no card do vendedor.
Evento `conversa.nova` do adaptador (contato que nunca falou com o número) → `criarLead` com
`origem.canal = 'whatsapp'`, `origem` preenchida a partir da referência do anúncio quando existir
(`referral`/`externalAdReply`: campanha, anúncio, ctwaClid), `consentimento.tipo = 'mensagem_espontanea'`
com o texto e a data da primeira mensagem como evidência → card em **Novo** → distribuição imediata.
Na fase 2 o adaptador `whatsapp` é `local` com um botão "Simular conversa nova" só em modo dev.

### 4.3 Lead Ads (contrato pronto, adaptador `local`)
Evento `lead.novo` com `canal = 'lead_ads'`, campos do formulário em `camposFormulario`,
`consentimento.tipo = 'formulario'`. Tela de integração Meta lista formulários e mostra o último lead
recebido por formulário.

## 5. Distribuição automática (`/configuracoes/distribuicao`, só gestor)

Formulário: modo (rodízio / por região / manual), limite de cards abertos por vendedor, minutos até
devolver à fila sem contato, horário de funcionamento por dia, o que fazer fora do horário (fila ou
IA, IA só a partir da fase 5), vendedores participantes com regiões (DDDs) por pessoa. Prévia:
"Com estas regras, o próximo lead vai para: <nome>".
Comportamento: card novo recebe vendedor na hora; notificação no shell ("Novo lead para você:
<nome>, <cidade>") com botão Ligar; sem contato em N minutos → volta para a fila, registra movimento
"sistema" e notifica o gestor.

## 6. Cadência e próximo passo

Resultado `nao_atendeu`/`caixa_postal`/`ocupado` agenda automaticamente uma retentativa (padrão: +2 h,
+1 dia, +3 dias; configurável) e oferece **"Enviar WhatsApp de fallback"** com modelo editável. O
próximo passo aparece no card e numa lista **"Minha fila de hoje"** (`/leads/fila`) ordenada por
horário, com botão Ligar em cada item e "Próximo da fila" integrado ao modo power do discador.

## 7. Integração com o discador (já existe)

Ao desligar uma chamada aberta por `openDialer` com `leadId`, o discador emite `chamada.encerrada`
com resultado escolhido, duração e URL da gravação; o kanban grava a `Interacao`, incrementa
tentativas quando aplicável, move o card (regras de adjacência) e agenda a cadência.

## 8. Critérios de aceite (checklist do PR)

- [ ] Cinco colunas com contadores e SLA; filtros e busca funcionando; cards com todos os campos.
- [ ] Arrastar só adjacente; motivos obrigatórios; rollback em falha; acessível por teclado.
- [ ] Drawer com os três blocos, histórico de movimentos, linha do tempo e consentimento; edição inline.
- [ ] Importação da planilha de 540 leads com deduplicação e mapa de resultado; relatório final.
- [ ] Conexão por QR com estados; conversa nova simulada gera card em Novo já atribuído.
- [ ] Regras de distribuição salvas e aplicadas; devolução à fila por tempo; notificação no shell.
- [ ] Cadência agendando retentativa e "Minha fila de hoje" com Ligar e Próximo da fila.
- [ ] Ligar no card abre o discador com o número; ao desligar, resultado vira interação e move o card.
- [ ] Selo "Dados de demonstração" visível onde o adaptador for `local`; nenhum mock sem selo.
- [ ] README com o contrato do adaptador `crm` e do evento `conversa.nova` para o backend.
